# from apps.app import db
from app import db
from apps.crud.models import User
from flask import Blueprint, render_template, redirect, url_for
from apps.crud.forms import UserForm


# Blueprint로 crud 앱을 생성한다
board = Blueprint(
    "board",
    __name__,
    template_folder="templates",
    static_folder="static", 
)


# index 엔드포인트를 작성하고 index.html을 반환한다
@board.route("/")
def index():
    return render_template("board/index.html") 
