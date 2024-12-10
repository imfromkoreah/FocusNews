from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy 인스턴스 생성
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # SQLite3 데이터베이스 설정
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testdb.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
