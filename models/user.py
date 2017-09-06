from . import db, ModelMixin, unix_time
from random import randint
from werkzeug.security import generate_password_hash, check_password_hash


class UserCls(db.Model, ModelMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hashed = db.Column(db.String(200))
    email = db.Column(db.String(64), default='')
    created_time = db.Column(db.String(64), default='')
    avatar = db.Column(db.String(100))
    topics = db.relationship('TopicCls', foreign_keys='TopicCls.user_id',
                             backref='user_ref', lazy='dynamic')
    #backref=db.backref('user_ref', lazy='dynamic'),    backref='user_ref',

    newupdate_topics = db.relationship('TopicCls', foreign_keys='TopicCls.replyuser_id',
                                       backref='lastreplyer_ref', lazy='dynamic')
    comment_out = db.relationship('CommentCls', foreign_keys='CommentCls.sender_id',
                                   backref='sender_ref')
    comment_in = db.relationship('CommentCls', foreign_keys='CommentCls.receiver_id',
                                  backref='receiver_ref')
    topic_collection = db.relationship('TopicCollection', backref='user_ref',
                                       lazy='dynamic', order_by='desc(TopicCollection.id)')


    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.email = form.get('email', '')

    def get_created_time(self):
        self.created_time = unix_time()

    def get_avatar(self):
        i = randint(0, 10)
        self.avatar = '/static/img/avatar/avatar_default{}.png'.format(i)

    def validate_login(self):
        u = UserCls.query.filter_by(username=self.username).first()
        if u is None:
            return False
        else:
            return check_password_hash(u.password_hashed, self.password)

    def is_admin(self):
        return self.id == 1

    def validate_register(self):
        u = UserCls.query.filter_by(username=self.username).first()
        isvalid_username = 2 < len(self.username) < 9
        isvalid_password = 2 < len(self.password) < 9
        if not u and isvalid_password and isvalid_password:
            self.password_hashed = generate_password_hash(self.password)
            self.get_avatar()
            self.get_created_time()
            self.save()
            return True
        else:
            return False

