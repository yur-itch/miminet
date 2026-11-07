"""Reproduce #542: creating a Test via flask-admin loses created_by_id.

Mirrors miminet's CreatedByMixin + MiminetAdminModelView.on_model_change and
posts the "create" form exactly like the admin UI does (author field left blank).
Runs against Postgres (DB_URL env) to match prod.
"""

import os
import sys

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import BigInteger, Boolean, ForeignKey, Text
from sqlalchemy.orm import declared_attr

CURRENT_USER_ID = 1

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DB_URL"]
app.config["SECRET_KEY"] = "x"
app.config["WTF_CSRF_ENABLED"] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(BigInteger, primary_key=True)
    nick = db.Column(Text, nullable=False)

    def __str__(self):
        return self.nick


class CreatedByMixin:
    @declared_attr
    def created_by_id(cls):
        return db.Column("created_by_id", ForeignKey("user.id"))

    @declared_attr
    def created_by_user(cls):
        return db.relationship("User")


class Test(CreatedByMixin, db.Model):
    __tablename__ = "test"
    id = db.Column(BigInteger, primary_key=True)
    is_deleted = db.Column(Boolean, default=False)
    name = db.Column(Text, default="Название теста")


class BaseView(ModelView):
    form_excluded_columns = ["is_deleted", "updated_on", "created_on"]

    def on_model_change(self, form, model, is_created, **kwargs):
        if hasattr(model, "created_by_id") and is_created:
            model.created_by_id = CURRENT_USER_ID


class TestViewAsInMain(BaseView):
    pass


class TestViewFixed(BaseView):
    form_excluded_columns = BaseView.form_excluded_columns + [
        "created_by_id",
        "created_by_user",
    ]


variant = sys.argv[1]
view_cls = {"main": TestViewAsInMain, "fixed": TestViewFixed}[variant]
admin = Admin(app)
admin.add_view(view_cls(Test, db.session, endpoint="test", name="test"))

with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.add(User(id=CURRENT_USER_ID, nick="admin"))
    db.session.commit()

    client = app.test_client()
    form_html = client.get("/admin/test/new/").get_data(as_text=True)
    print(f"[{variant}] author field rendered in form:", "created_by_user" in form_html)

    resp = client.post("/admin/test/new/", data={"name": "t1"})
    print(f"[{variant}] POST status:", resp.status_code)

    db.session.expire_all()
    t = Test.query.first()
    print(f"[{variant}] created_by_id after create:", t.created_by_id if t else "NO ROW")
