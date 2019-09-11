"""Access Service"""

import time
import json

from urllib.parse import urljoin, urlencode

import requests

from nameko.rpc import rpc, RpcProxy
from nameko.dependency_providers import Config
from nameko.extensions import DependencyProvider

import jwt


class PlayerREST:
    host = "player"
    port = 8000

    def _get_url(self, path):
        return urljoin(f"http://{self.host}:{self.port}/", path)

    def post(self, path: str, payload: dict):
        headers = {
            'Content-Type': 'application/json'
        }
        req = requests.post(self._get_url(path), json=payload, headers=headers)
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
    def signup(self, username, password, country):
        return self.player_rpc.create_player(username, password, country, 1000)
