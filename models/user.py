from . import db, ModelMixin

class UserCls(db.Model, ModelMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))
    #mail = db.Column(db.String(64))
   # topic = db.relationship('TopicCls', backref='user_ref')

    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def validate_login(self):
        u = UserCls.query.filter_by(username=self.username).first()
        if u is None:
            return False
        else:
            return self.username == u.username and self.password == u.password

    def validate_register(self):
        u = UserCls.query.filter_by(username=self.username).first()
        if u is not None:
            return False
        else:
            return len(self.username) > 3 and len(self.password) > 2

