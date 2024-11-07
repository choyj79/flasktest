from pathlib import Path
from flask import Flask, Blueprint,render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from apps.config import config
from flask_login import LoginManager



# LoginManager를 인스턴스화 한다.
login_manager = LoginManager()
login_manager.login_view = "acct.signup"
login_manager.login_message = ""

# SQLAlchemy를 인스턴스화 하기
db = SQLAlchemy()
csrf = CSRFProtect()


def create_app(config_key):
    # 플라스크 객체(인스턴스) 생성
    app = Flask(__name__)

    # 기본 라우트 추가
    # @app.route('/')
    # def index():
    #     return render_template('main.html')

    # 앱의 config 설정
    app.config.from_object(config[config_key])

    # 앱과 연계하기
    csrf.init_app(app)
    db.init_app(app)

    # Migrate와 앱을 연계한다
    migrate = Migrate(app, db)
    
    #login_manager를 애플리케이션화 연계하기
    login_manager.init_app(app)

    # 블루프린트 등록
    from apps.crud import views as crud_views
    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    from apps.board import views as board_views
    app.register_blueprint(board_views.board, url_prefix="/board")

    from apps.auth import views as auth_views
    app.register_blueprint(auth_views.auth, url_prefix="/auth")
    
    from apps.acct import views as acct_views
    app.register_blueprint(acct_views.acct, url_prefix="/acct")

    from apps.main import views as main_views
    app.register_blueprint(main_views.main, url_prefix="/main")

    return app