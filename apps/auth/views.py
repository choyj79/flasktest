# from apps.app import db
from app import db
from apps.crud.models import UserTest
from flask import Blueprint, render_template, redirect, url_for
from apps.crud.forms import UserForm


# Blueprint로 crud 앱을 생성한다
auth = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
    static_folder="static", 
)


# index 엔드포인트를 작성하고 index.html을 반환한다
@auth.route("/")
def index():
    return render_template("auth/index.html") 

@auth.route("/users/new", methods=["GET", "POST"])
def create_user():
    # UserForm을 인스턴스화한다
    form = UserForm()

    # 폼의 값을 벨리데이트한다
    if form.validate_on_submit():
        # 사용자를 작성한다
        user = UserTest(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )

        # 사용자를 추가하고 커밋한다
        db.session.add(user)
        db.session.commit()

        # 사용자의 일람 화면으로 리다이렉트한다
        return redirect(url_for("auth.users"))
    return render_template("auth/create.html", form=form)

@auth.route('/users')
def users():
    #사용자의 일람을 취득
    users = UserTest.query.all()
    print(users)
    return render_template('auth/index.html',users=users)

@auth.route('/user/<user_id>',methods=["POST","GET"])
def edit_user(user_id):
    form = UserForm() #유효성 검사를 위한 객체 생성하기
    user = UserTest.query.filter_by(id=user_id).first() #데이터 얻기
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("auth.users"))
    return render_template('auth/edit.html',user=user, form=form)


@auth.route("/sql")
def sql():
    db.session.query(UserTest).all()
    # db.session.query(User).first()
    # db.session.query(User).get(2)
    # db.session.query(User).count()
    # User.query.paginate(page=None, per_page=None, error_out=True)
    # db.session.query(User).filter_by(id=2, username="admin").all()
    # db.session.query(User).filter(User.id==2, User.username == "admin").all()
    # db.session.query(User).limit(1).all()
    # db.session.query(User).limit(1).offset(2).all()
    # db.session.query(User).order_by("username").all()
    # db.session.query(User).group_by("username").all()
    # user = User(
    #     username ="jojju",
    #     email = "jojju@naver.com",
    #     password="1234"
    # ) #사용자 모델 객체 생성
    # db.session.add(user) #사용자 추가하기
    # db.session.commit()  #커밋하기
    # user = db.session.query(User).filter_by(id=1).first()
    # user.username = "jojju486"
    # user.email = "jojju486@gmail.com"
    # user.password = "1111"
    # db.session.add(user)
    # db.session.commit()
    # user = db.session.query(User).filter_by(id=1).delete()
    db.session.commit()
    return "콘솔 확인1"

