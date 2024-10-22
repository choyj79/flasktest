from app import db
# from apps.app import db
from apps.crud.models import User
from flask import Blueprint, render_template, redirect, url_for
from apps.crud.forms import UserForm


# Blueprint로 crud 앱을 생성한다
crud = Blueprint(
    "crud",
    __name__,
    template_folder="templates",
    static_folder="static", 
)

# index 엔드포인트를 작성하고 index.html을 반환한다
@crud.route("/")
def index():
    return render_template("crud/index.html") 

@crud.route("/sql")
def sql():
    # db.session.query(User).all()
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

@crud.route("/users/new", methods=["GET", "POST"])
def create_user():
    # UserForm을 인스턴스화한다
    form = UserForm()

    # 폼의 값을 벨리데이트한다
    if form.validate_on_submit():
        # 사용자를 작성한다
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )

        # 사용자를 추가하고 커밋한다
        db.session.add(user)
        db.session.commit()

        # 사용자의 일람 화면으로 리다이렉트한다
        return redirect(url_for("crud.users"))
    return render_template("crud/create.html", form=form)

@crud.route('/users')
def users():
    #사용자의 일람을 취득
    users = User.query.all()
    print(users)
    return render_template('crud/index.html',users=users)
#사용자 편집 화면 엔드포인트
@crud.route('/user/<user_id>',methods=["GET","POST"])
def edit_user(user_id):
    form = UserForm() #객체 생성하기
    user = User.query.filter_by(id=user_id).first() #사용자 취득
    #form으로부터 제출된 사용자를 갱신하여 일람 화면으로 리다이렉트
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("crud.users"))
    return render_template('crud/edit.html',user=user, form=form)

#사용자 삭제 화면
@crud.route('/user/<user_id>/delete',methods=["POST"])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('crud.users'))