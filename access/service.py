"""Access Service"""

import requests
import json

from nameko.rpc import rpc, RpcProxy
from nameko.dependency_providers import Config
from nameko.extensions import DependencyProvider

from urllib.parse import urljoin
import jwt

import time
import json


class PlayerREST:
    host = "player"
    port = 8000

    def _get_url(self, path):
        return urljoin(f"http://{self.host}:{self.port}/", path)

    def post(self, path: str, payload: dict):
        req = requests.post(self._get_url(path), json=json.dumps(payload))
        return {
            "content": req.content,
            "status_code": req.status_code
        }

    def get(self, path: str):
        req = requests.get(self._get_url(path))
        return {
            "content": req.content,
            "status_code": req.status_code
        }


class PlayerRESTProvider(DependencyProvider):
    def get_dependency(self, worker_ctx):
        return PlayerREST()


class AccessService:
    name = 'access'

    player_rpc = RpcProxy("player")
    player_rest = PlayerRESTProvider()
    auth = RpcProxy("access")

    config = Config()

    @rpc
    def login(self, username, password):

        player = self.player_rpc.get_player(username, password)

        if player is None:
            return None

        jwt_secret = self.config.get("JWT_SECRET", "secret")

        token = jwt.encode({
            'username': player["username"],
            "exp": time.time() + 60
        }, jwt_secret, algorithm='HS256')
        return json.dumps({"jwt": token.decode(), "user": player})

    @rpc
    def signup(self, username, password):

        data = {
            "username": username,
            "password": password,
            "country": "Chile",
            "elo": 1000
        }

        req = self.player_rest.post("/player", data)

        if req["status_code"] == 200:
            return True
        return False
