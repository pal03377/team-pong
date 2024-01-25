from flask import Flask, redirect, jsonify, request
from flask_socketio import SocketIO, join_room
from flask_cors import *
import dataset
import random
import asyncio
import threading
import math
from .helpers.board_config import BoardConfig

app = Flask(
    __name__,
    static_folder="../../../frontend/public",
    static_url_path="/static",
)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*") # , engineio_logger=True, logger=True)
db = dataset.connect(
    'sqlite:///db.sqlite', engine_kwargs={"connect_args": {'check_same_thread': False}})

teams = db["teams"]
TEAMS = ["A", "B"]
for team in TEAMS:
    teams.upsert(dict(team=team, count=0, y=0), ["team"])
def get_team_count(team):
    return teams.find_one(team=team)["count"]
def get_min_team_count():
    return min(get_team_count(t) for t in TEAMS)

countdown = db["countdown"]
def get_countdown():
    return countdown.find_one()["count"]
def set_countdown(to):
    countdown.upsert(dict(count=to), [])
set_countdown(-1)


balls = db["balls"]
balls.delete()

config_db = db.create_table('config', primary_type=db.types.text)
board_config = BoardConfig(config_db)


def broadcast_teams():
    socketio.emit("teams", [dict(t) for t in teams.all()])

@app.get("/weakest_teams")
def get_weakest_teams():
    return jsonify(list([team for team in TEAMS if get_team_count(team) == get_min_team_count()]))

@socketio.on("join")
def on_join(team):
    print(f"someone from team {team} has entered")
    teams.upsert(dict(team=team, count=teams.find_one(team=team)["count"] + 1), ["team"])
    broadcast_teams()


@socketio.on("join_board")
def on_join_board():
    print("board joined")
    join_room("board")
    broadcast_data()


def request_rejoin():
    # kick everyone out and request them to rejoin
    # because a leaving mechanism doesn't really work
    teams.update(dict(count=0), [])
    broadcast_teams()
    socketio.emit("rejoin_request")


@socketio.on("up")
def up(team):
    new_y = teams.find_one(team=team)["y"] + board_config.platform_movement_speed
    if new_y > board_config.max_abs_platform_y:
        new_y = board_config.max_abs_platform_y
    teams.upsert(dict(team=team, y=new_y), ["team"])
    broadcast_teams()

@socketio.on("down")
def down(team):
    new_y = teams.find_one(team=team)["y"] - board_config.platform_movement_speed
    if new_y < -board_config.max_abs_platform_y:
        new_y = -board_config.max_abs_platform_y
    teams.upsert(dict(team=team, y=new_y), ["team"])
    broadcast_teams()


def broadcast_countdown():
    socketio.emit("countdown", get_countdown())

def broadcast_balls():
    # balls are only broadcast to the board
    socketio.emit("balls", [dict(b) for b in balls.all()], room="board")

def add_ball(direction=None):
    if direction is None:
        direction = random.choice([-1, 1])
    ball = dict(
        x=0, y=0,
        vx=direction * board_config.ball_speed_factor,
        vy=(random.random() * 2 - 1) * board_config.ball_speed_factor,
    )
    balls.insert(ball)
    broadcast_balls()
    return ball

def win(team):
    socketio.emit("win", team)
    teams.update(dict(team=team, score=teams.find_one(team=team)["score"] + 1), ["team"])
    balls.delete()
    broadcast_teams()
    broadcast_balls()

def blop():
    # trigger blop sound for board
    if board_config.blop_sound_enabled:
        socketio.emit("blop", room="board")

def sign(n):
    return 1 if n > 0 else -1 if n < 0 else 0

def check_win_conditions(ball):
    if ball["x"] < -100:
        win("B")
        return True
    if ball["x"] > 100:
        win("A")
        return True
    return False

def vertical_bounce(ball):
    if ball["y"] < -20:
        ball["vy"] = abs(ball["vy"])
        blop()
    if ball["y"] > 20:
        ball["vy"] = -abs(ball["vy"])
        blop()

def get_relative_intersect(ball):
    # get the distance of the ball to the center of the platform
    # the ball is on
    if ball["x"] < 0:
        return abs(ball["y"] - teams.find_one(team="A")["y"])
    else:
        return abs(ball["y"] - teams.find_one(team="B")["y"])


# ball bounce mechanics from https://gamedev.stackexchange.com/a/4255/97861
def get_relative_intersect_normalized(ball):
    return get_relative_intersect(ball) / board_config.platform_height * 2

def get_ball_bounce_angle(ball):
    return get_relative_intersect_normalized(ball) * math.pi / 3 # max 60 degrees

def get_speedboost(ball):
    return abs(get_relative_intersect_normalized(ball)) * (board_config.max_ball_speed_factor - board_config.ball_speed_factor)

def get_new_ball_speed_positive(ball):
    speed_factor = board_config.ball_speed_factor
    speed_factor += get_speedboost(ball)
    vx = speed_factor * math.cos(get_ball_bounce_angle(ball))
    vy = speed_factor * math.sin(get_ball_bounce_angle(ball))
    return vx, vy

def negate_velocities(v):
    return -v[0], -v[1]

def platform_bounce_ball(ball):
    vy_sign_before = sign(ball["vy"])
    if ball["x"] < 0:
        ball["vx"], ball["vy"] = get_new_ball_speed_positive(ball)
        # make sure that the ball is outside now
        ball["x"] = -89.9
    else:
        ball["vx"], ball["vy"] = negate_velocities(get_new_ball_speed_positive(ball))
        # make sure that the ball is outside now
        ball["x"] = 89.9
    # difference to actual game: vy sign will always be the same
    if vy_sign_before != sign(ball["vy"]):
        ball["vy"] = -ball["vy"]
    blop()

def platform_bounce(ball):
    # bounce off of platforms
    # platforms are between -100 to -95 and 95 to 100
    left_platform_y = teams.find_one(team="A")["y"]
    right_platform_y = teams.find_one(team="B")["y"]
    if ball["x"] < -90 and ball["x"] > -95 and abs(get_relative_intersect_normalized(ball)) < 1:
        platform_bounce_ball(ball)
    if ball["x"] > 90 and ball["x"] < 95 and abs(get_relative_intersect_normalized(ball)) < 1:
        platform_bounce_ball(ball)

def update_balls():
    """Returns whether to end the running game (because someone won)"""
    for ball in balls.all():
        ball = dict(ball)
        ball["x"] += ball["vx"]
        ball["y"] += ball["vy"]
        if check_win_conditions(ball):
            return True
        vertical_bounce(ball)
        platform_bounce(ball)
        balls.upsert(ball, ["id"])
    broadcast_balls()
    return False


@app.route("/")
def get_home():
    return redirect("/static/index.html", code=302)


@app.route("/reset", methods=["POST"])
def reset():
    for team in TEAMS:
        teams.upsert(dict(team=team, count=0, y=0, score=0), ["team"])
    balls.delete()
    set_countdown(-1)
    return "ok"


@app.route("/config")
def get_config():
    return jsonify(board_config.to_dict())


def broadcast_config():
    socketio.emit("config", board_config.to_dict())


@app.route("/config", methods=["POST"])
def set_config():
    board_config.update_from_dict(request.json)
    broadcast_config()
    return "ok"


async def waiting_gameloop():
    print("----- waiting gameloop -----")
    counter = 0
    while True:
        if counter % 8 == 0:
            request_rejoin() # nice to do that sometimes (more often than every countdown cycle)
        counter += 1
        await asyncio.sleep(1)
        if all(get_team_count(t) >= board_config.min_player_number_per_team for t in TEAMS):
            print(f"countdown: {get_countdown()}")
            if get_countdown() < 0:
                set_countdown(board_config.countdown)
            else:
                set_countdown(get_countdown() - 1)
                if get_countdown() <= 0:
                    set_countdown(-1)
                    return # game will be started
        else:
            set_countdown(-1)
        broadcast_countdown()

async def running_gameloop():
    print("----- running gameloop -----")
    while True:
        await asyncio.sleep(0.1)
        someone_won = update_balls()
        if someone_won:
            return # game will be ended

def start_game():
    print("START!")
    socketio.emit("start")
    # guarantee that balls fly in different directions
    initial_direction = random.choice([-1, 1])
    other_direction = -initial_direction
    for i in range(board_config.number_of_balls):
        add_ball(direction=initial_direction if i % 2 == 0 else other_direction)
    blop()

def end_game():
    print("END!")
    socketio.emit("end")

def broadcast_data():
    broadcast_teams()
    broadcast_balls()
    broadcast_countdown()

async def gameloop():
    while True:
        broadcast_data()
        await waiting_gameloop()
        start_game()
        broadcast_data()
        await running_gameloop()
        end_game()


@app.before_first_request
def start_gameloop_thread():
    _thread = threading.Thread(target=asyncio.run, args=(gameloop(),))
    _thread.start()


if __name__ == "__main__":
    import os
    socketio.run(
        app, 
        host="0.0.0.0", 
        port=os.env.get("PORT", 5109), 
        debug=True, 
        use_reloader=True,
    )
