from email_validator import EmailNotValidError, validate_email
from flask import Flask, render_template, url_for, current_app, g, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
import logging

app = Flask(__name__)

#secret_key를 추가
app.config["SECRET_KEY"] = "2AZSMss3p5QPbcY2hBsJ"

#로그레벨을 설정
app.logger.setLevel(logging.DEBUG)

# 리다이렉트를 중단하지 않도록 한다
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

# DebugToolbarExtension에 애플리케이션을 세트한다
toolbar = DebugToolbarExtension(app)

@app.route("/")
def index():
    return "Hello, Flaskbook!" 

@app.route("/hello/<name>", methods=['GET','POST'], endpoint='hello-endpoint')
def hello(name):
    return f"Hello, {name}!"

@app.route("/name/<name>")
def show_name(name):
    return render_template('index.html', name=name)

with app.test_request_context():
    print(url_for('index'))
    print(url_for('hello-endpoint', name = 'world'))
    print(url_for('show_name', name = 'AK', page='1'))
    
# 여기에서 호출하면 오류가 된다
# print(current_app)

# 애플리케이션 컨텍스트를 취득하여 스택에 push한다
ctx = app.app_context()
ctx.push()

# current_app에 접근이 가능해진다
print(current_app.name)
# >> apps.minimalapp.app

# 전역 임시 영역에 값을 설정한다
g.connection = "connection"
print(g.connection)
# >> connection

with app.test_request_context("/users?updated=true"):
    # true가 출력된다
    print(request.args.get("updated"))
    
@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/contact/complete", methods=['GET','POST'])
def contact_complete():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]
        
        # 입력 체크
        is_valid = True
        if not username:
            flash("사용자명은 필수입니다")
            is_valid = False

        if not email:
            flash("메일 주소는 필수입니다")
            is_valid = False

        try:
            validate_email(email)
        except EmailNotValidError:
            flash("메일 주소의 형식으로 입력해 주세요")
            is_valid = False

        if not description:
            flash("문의 내용은 필수입니다")
            is_valid = False

        if not is_valid:
            return redirect(url_for("contact"))
        
        flash("문의해 주셔서 감사합니다.")        
        return redirect(url_for('contact_complete'))
    
    return render_template('contact_complete.html')

app.logger.critical("fatal error")
app.logger.error("error")
app.logger.warning("warning")
app.logger.info("info")
app.logger.debug("debug")
