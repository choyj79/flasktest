# from apps.app import db
from app import db
from apps.acct.forms import SignUpForm, LoginForm
from apps.crud.models import User
from flask import Blueprint, render_template, redirect, url_for, flash, request,session
from apps.crud.forms import UserForm
from flask_login import login_user, logout_user


# Blueprint로 crud 앱을 생성한다
acct = Blueprint(
    "acct",
    __name__,
    template_folder="templates",
    static_folder="static", 
)

# index 엔드포인트를 작성하고 index.html을 반환한다
@acct.route("/")
def index():
    return render_template("acct/index.html") 

@acct.route("/signup",methods=["GET","POST"])
def signup():
    # SignUpForm을 인스턴스화한다
    form = SignUpForm()

    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )

        # 메일 주소 중복 체크를 한다
        if user.is_duplicate_email():
            flash("지정한 이메일 주소는 이미 등록되어 있습니다.")
            return redirect(url_for("acct.signup"))

        # 사용자 정보를 등록한다
        db.session.add(user)
        db.session.commit()

        # 사용자 정보를 세션에 저장한다
        login_user(user)

        # GET 파라미터에 next 키가 존재하고, 값이 없는 경우는 사용자의 일람 페이지로 리다이렉트한다
        next_ = request.args.get("next")
        if next_ is None or not next_.startswith("/"):
            next_ = url_for("acct.index")
        return redirect(next_)

    return render_template("acct/signup.html", form=form)

@acct.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # 메일 주소로부터 사용자를 취득한다
        user = User.query.filter_by(email=form.email.data).first()

        # 사용자가 존재하고 비밀번호가 일치하는 경우는 로그인을 허가한다
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for("crud.users"))

        # 로그인 실패 메시지를 설정한다
        flash("메일 주소 또는 비밀번호가 일치하지 않습니다")
    return render_template("acct/login.html", form=form) 

@acct.route("/logout")
def logout():
    logout_user()
    session.clear()  # 세션 데이터 초기화 (모든 flash 메시지 포함)
    flash("로그아웃되었습니다.", "info")  # 원하는 메시지를 설정할 수도 있습니다
    return redirect(url_for("acct.login"))
