"""Regression tests for Yandex sign-up (issue #539).

New Yandex users got neither their profile picture nor the example network
that VK sign-up creates.
"""

from types import SimpleNamespace

import pytest
import requests

import miminet_auth
from app import app as flask_app

YANDEX_JSON = {
    "web": {
        "client_id": "id",
        "client_secret": "secret",
        "redirect_uris": ["http://localhost/auth/yandex_callback"],
        "token_uri": "https://oauth.yandex.ru/token",
    }
}


def test_yandex_avatar_url_from_default_avatar_id():
    info = {"default_avatar_id": "131652443/kt9Gx", "is_avatar_empty": False}

    assert (
        miminet_auth.yandex_avatar_url(info)
        == "https://avatars.yandex.net/get-yapic/131652443/kt9Gx/islands-200"
    )


@pytest.mark.parametrize(
    "info",
    [
        {"default_avatar_id": "0/0-0", "is_avatar_empty": True},  # placeholder
        {},  # app has no "profile picture" permission
    ],
    ids=["placeholder", "no-permission"],
)
def test_yandex_avatar_url_none_without_real_picture(info):
    assert miminet_auth.yandex_avatar_url(info) is None


def test_download_avatar_saves_picture(mocker):
    get = mocker.patch("miminet_auth.requests.get")
    get.return_value.content = b"png"
    save = mocker.patch("miminet_auth.save_avatar_blob")

    avatar_uri = miminet_auth.download_avatar("https://pic", "Yandex", "42")

    assert avatar_uri != "empty.jpg"
    save.assert_called_once_with(avatar_uri, b"png")


def test_download_avatar_falls_back_on_network_error(mocker):
    mocker.patch(
        "miminet_auth.requests.get", side_effect=requests.ConnectionError("down")
    )
    save = mocker.patch("miminet_auth.save_avatar_blob")

    assert miminet_auth.download_avatar("https://pic", "Yandex", "42") == "empty.jpg"
    save.assert_not_called()


@pytest.fixture
def yandex_login(mocker):
    """Run yandex_callback with Yandex OAuth, the DB and token issuing mocked."""

    def run(id_info, existing_user=None):
        oauth = mocker.patch("miminet_auth.OAuth2Session").return_value
        oauth.get.return_value.json.return_value = id_info
        mocker.patch("miminet_auth._bind_social_account", return_value=None)
        mocker.patch("miminet_auth.db")
        mocker.patch("miminet_auth.login_user")
        mocker.patch("miminet_auth.create_access_token", return_value="a")
        mocker.patch("miminet_auth.create_refresh_token", return_value="r")
        mocker.patch("miminet_auth.issue_jwt_cookies")

        created_user = SimpleNamespace(id=7)
        user_model = mocker.patch("miminet_auth.User")
        user_model.query.filter_by.return_value.first.side_effect = (
            [existing_user] if existing_user else [None, created_user]
        )
        download = mocker.patch(
            "miminet_auth.download_avatar", return_value="a/b/ab.jpg"
        )
        example = mocker.patch("miminet_auth.create_example_network")

        with flask_app.test_request_context("/auth/yandex_callback?code=c&state=s"):
            miminet_auth.session["state"] = "s"
            miminet_auth.yandex_callback(yandex_json=YANDEX_JSON)

        return SimpleNamespace(
            user_model=user_model,
            created_user=created_user,
            download=download,
            example=example,
        )

    return run


def test_new_yandex_user_gets_avatar_and_example_network(yandex_login):
    result = yandex_login(
        {
            "id": "42",
            "login": "student",
            "default_email": "s@ya.ru",
            "default_avatar_id": "131652443/kt9Gx",
            "is_avatar_empty": False,
        }
    )

    result.download.assert_called_once_with(
        "https://avatars.yandex.net/get-yapic/131652443/kt9Gx/islands-200",
        "Yandex",
        "42",
    )
    assert result.user_model.call_args.kwargs["avatar_uri"] == "a/b/ab.jpg"
    result.example.assert_called_once_with(result.created_user)


def test_new_yandex_user_without_picture_keeps_default_avatar(yandex_login):
    result = yandex_login({"id": "42", "login": "student", "is_avatar_empty": True})

    result.download.assert_not_called()
    assert result.user_model.call_args.kwargs["avatar_uri"] == "empty.jpg"
    result.example.assert_called_once_with(result.created_user)


def test_returning_yandex_user_gets_no_second_example_network(yandex_login):
    result = yandex_login(
        {"id": "42", "login": "student"}, existing_user=SimpleNamespace(id=7)
    )

    result.download.assert_not_called()
    result.example.assert_not_called()
    result.user_model.assert_not_called()  # no new User row
