import sqlalchemy
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from .db_session import SqlAlchemyBase
from datetime import datetime


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    password = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    surname = sqlalchemy.Column(sqlalchemy.String)
    patronymic = sqlalchemy.Column(sqlalchemy.String)
    teacher = sqlalchemy.Column(sqlalchemy.Boolean)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.now)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
