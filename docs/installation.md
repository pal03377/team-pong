# Installation

I suggest using the docker-compose configuration provided in the `backend` folder. You can also run the backend and frontend separately while developing.

## Using Docker for Deployment
1. Install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/gettingstarted/).
2. Run `docker compose up --build` in the `backend` folder to verify that everything works. This will build the frontend and start up the server.
3. The Docker setup has two variables to configure. The first is the `PORT` environment variable which is used to configure the port the server listens on. The second is the `LEGAL_LINK` environment variable which is used to configure the URL the clients (with the arrows) will show for the "Imprint & Privacy Policy" link. When starting the containers manually, you can set them using `PORT=8080 LEGAL_LINK=https://example.com docker-compose up --build`. By default, the port is **5109** and the legal link is not set, which means that the link will not be shown.
4. Set up an internal redirect from the port you configured to the port the server listens on (5109 by default). The difficult part is making sure that `/socket.io` websocket connections don't get lost. Caddyserver does this automatically, so I suggest to use Caddy.
5. There are instructions on how to open the board below. Enjoy!

## Local Development Setup
1. Install [Node.js](https://nodejs.org/en/download/) and [Python 3](https://www.python.org/downloads/).
2. Run `npm install` in the `frontend` folder to install the dependencies.
3. Run `python -m venv venv && source venv/bin/activate && pip install -r requirements.txt` in the `backend` folder to install the dependencies.
3. Run `npm start` in the `frontend` folder to build and watch the frontend.
4. Run `./start-backend.sh` in the `backend` folder to start the backend.