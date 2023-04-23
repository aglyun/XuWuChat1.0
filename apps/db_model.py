from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)    # 数据库ID
    username = db.Column(db.String(16), nullable=False, unique=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(64), nullable=True)  # 邮箱