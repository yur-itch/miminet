"""#539 end-to-end on the local DB: Yandex callback with only the OAuth exchange faked."""
import os
import sys
import time
from unittest import mock

avatar_dir = sys.argv[1]
import miminet_auth  # noqa: E402  (cwd = front/src, on sys.path)
from app import app  # noqa: E402
from miminet_model import Network, User  # noqa: E402

yandex_id = f"ya-{int(time.time())}"
id_info = {"id": yandex_id, "login": "ya_student", "default_email": f"{yandex_id}@ya.ru",
           "default_avatar_id": "0/0-0", "is_avatar_empty": False}
yandex_json = {"web": {"client_id": "i", "client_secret": "s", "token_uri": "https://oauth.yandex.ru/token",
                       "redirect_uris": ["http://127.0.0.1/auth/yandex_callback"], "auth_uri": "x"}}

with mock.patch.object(miminet_auth, "AVATAR_UPLOAD_FOLDER", avatar_dir), \
     mock.patch.object(miminet_auth, "OAuth2Session") as oauth:
    oauth.return_value.get.return_value.json.return_value = id_info
    with app.test_request_context("/auth/yandex_callback?code=c&state=s"):
        miminet_auth.session["state"] = "s"
        resp = miminet_auth.yandex_callback(yandex_json=yandex_json)
        print("callback ->", resp.status_code, resp.headers.get("Location"))
        user = User.query.filter_by(yandex_id=yandex_id).first()
        print("user:", user.id, user.nick, "| avatar_uri:", user.avatar_uri)
        path = os.path.join(avatar_dir, user.avatar_uri)
        print("avatar file:", os.path.exists(path), os.path.getsize(path) if os.path.exists(path) else 0, "bytes")
        nets = Network.query.filter_by(author_id=user.id).all()
        print("networks:", [(n.title, n.preview_uri) for n in nets])
