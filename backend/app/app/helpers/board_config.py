from sqlalchemy import Column, Integer, String


class BoardConfig:
    def __init__(self, config_db):
        self.config_db = config_db
    def _get_property(self, property_name, default=None):
        row = self.config_db.find_one(id=property_name)
        if row is None:
            return default
        return row["value"]
    @property
    def language(self):
        return self._get_property("language", "en")
    @property
    def min_player_number_per_team(self):
        return int(self._get_property("min_player_number_per_team", default=1))
    @property
    def platform_height(self):
        return float(self._get_property("platform_height", default=10))
    @property
    def platform_movement_speed(self):
        return float(self._get_property("platform_movement_speed", default=1.2))
    @property
    def number_of_balls(self):
        return int(self._get_property("number_of_balls", default=1))
    @property
    def ball_speed_factor(self):
        return float(self._get_property("ball_speed_factor", default=1.2))
    @property
    def max_ball_speed_factor(self):
        return float(self._get_property("max_ball_speed_factor", default=2.8))
    @property
    def countdown(self):
        return int(self._get_property("countdown", default=3))
    @property
    def max_abs_platform_y(self):
        return int(20 - self.platform_height / 2) + 1
    @property
    def tap_cooldown(self):
        return int(self._get_property("tap_cooldown", default=1500))
    @property
    def blop_sound_enabled(self):
        return bool(self._get_property("blop_sound_enabled", default=1))
    def to_dict(self):
        return dict(
            language=self.language,
            min_player_number_per_team=self.min_player_number_per_team,
            platform_height=self.platform_height,
            platform_movement_speed=self.platform_movement_speed,
            number_of_balls=self.number_of_balls,
            ball_speed_factor=self.ball_speed_factor,
            max_ball_speed_factor=self.max_ball_speed_factor,
            countdown=self.countdown,
            max_abs_platform_y=self.max_abs_platform_y,
            tap_cooldown=self.tap_cooldown,
            blop_sound_enabled=self.blop_sound_enabled,
        )
    def update_from_dict(self, config_dict):
        for key, value in config_dict.items():
            if type(value) == bool:
                value = int(value)
            self.config_db.upsert(
                dict(id="test", value="Test"),
                ["id"],
            )
            self.config_db.upsert(
                dict(id=key, value=value, ensure=True),
                ["id"],
            )