from flask_sqlalchemy import SQLAlchemy
from flask import Flask
app1 = Flask(__name__)
db = SQLAlchemy(app1)


class ModelMixin(object):
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class UserCls(db.Model, ModelMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))
    email = db.Column(db.String(64), default='')
    created_time = db.Column(db.String(64), default='')
    avatar = db.Column(db.String(100))
    #topics = db.relationship('TopicCls', backref='user_ref')

    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.email = form.get('email', '')

if __name__ == '__main__':
    print UserCls({'username': '123'})
    print dir(db.Model())