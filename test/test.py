import json

from nameko.testing.services import worker_factory
from access.service import AccessService

TEST_USERNAME = "TestUser"
TEST_USERNAME2 = "TestUser2"
TEST_PASSWORD = "secret"


def test_signup():
    service = worker_factory(AccessService)

    def post_player(path, payload):
        if payload["username"] == TEST_USERNAME:
            return {
                "content": None,
                "status_code": 200
            }
        elif payload["username"] == TEST_USERNAME2:
            return {
                "content": None,
                "status_code": 400
            }
        else:
            return {
                "content": None,
                "status_code": 500
            }

    service.player_rest.post.side_effect = post_player

    assert service.signup(TEST_USERNAME, TEST_PASSWORD)
    assert not service.signup(TEST_USERNAME2, TEST_PASSWORD)
    assert not service.signup("", TEST_PASSWORD)


def test_login():
    service = worker_factory(AccessService)

    service.player_rpc.get_player.side_effect = \
        lambda username, password: {
            "username": username
        } if username == TEST_USERNAME and password == TEST_PASSWORD else None

    service.config.get = lambda key, default: default

    assert service.login(TEST_USERNAME, TEST_PASSWORD) is not None
    assert service.login(TEST_USERNAME, "") is None
