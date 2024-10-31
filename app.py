from pathlib import Path
from flask import Flask, Blueprint,render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from apps.config import config  # 경로는 그대로 유지

# SQLAlchemy를 인스턴스화 하기
db = SQLAlchemy()
csrf = CSRFProtect()
# basedir = Path(__file__).parent

# #BaseConfig 클래스 작성하기
# class BaseConfig:
#     SECRET_KEY = "2AZSMss3p5QPbcY2hBsJ"
#     WTF_CSRF_SECRET_KEY = "AuwzyszU5sugKN7KZs6f"

# # BaseConfig 클래스를 상속하여 LocalConfig 클래스를 작성한다
# class LocalConfig(BaseConfig):
#     SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'local.sqlite'}"
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SQLALCHEMY_ECHO = True


# # BaseConfig 클래스를 상속하여 TestingConfig 클래스를 작성한다
# class TestingConfig(BaseConfig):
#     SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'testing.sqlite'}"
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     WTF_CSRF_ENABLED = False
#     # 이미지 업로드처에 tests/detector/images를 지정한다
#     UPLOAD_FOLDER = str(Path(basedir, "tests", "detector", "images"))


# # config 사전에 매핑한다
# config = {
#     "testing": TestingConfig,
#     "local": LocalConfig,
# }

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

    # 블루프린트 등록
    from apps.crud import views as crud_views
    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    from apps.board import views as board_views
    app.register_blueprint(board_views.board, url_prefix="/board")

    from apps.auth import views as auth_views
    app.register_blueprint(auth_views.auth, url_prefix="/auth")

    from apps.main import views as main_views
    app.register_blueprint(main_views.main, url_prefix="/main")

    return app