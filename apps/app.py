from pathlib import Path
from flask import Flask, Blueprint
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect #CSRFProtect import하기
from apps.config import config

#SQLAlchemy를 인스턴스화 하기
db = SQLAlchemy()
csrf = CSRFProtect() #객체생성하기

def create_app(config_key):
    
    # 플라스크 객체(인스턴스) 생성
    app = Flask(__name__)
    
    #앱의 config 설정
    app.config.from_object(config[config_key])
    #앱과 연계하기
    csrf.init_app(app) 
    
    # SQLAlchemy와 앱을 연계한
    db.init_app(app)    
    
    # Migrate와 앱을 연계한다
    Migrate(app, db)
    
    # crud 패키지로부터 views를 import한다
    from apps.crud import views as crud_views
    
    #register_blueprint를 사용해 views 의 curd를 앱에 등록
    app.register_blueprint(crud_views.crud, url_prefix="/crud")     
    
    # board 패키지로부터 views를 import한다
    from apps.board import views as board_views
    
    #register_blueprint를 사용해 views 의 board를 앱에 등록
    app.register_blueprint(board_views.board, url_prefix="/board") 
    
    # auth 패키지로부터 views를 import한다
    from apps.auth import views as auth_views
    
    #register_blueprint를 사용해 views 의 auth를 앱에 등록
    app.register_blueprint(auth_views.auth, url_prefix="/auth") 
    
    # main 패키지로부터 views를 import한다
    from apps.main import views as main_views
    
    #register_blueprint를 사용해 views 의 main 앱에 등록
    app.register_blueprint(main_views.main, url_prefix="/main") 
        
    return app
