from . import db, ModelMixin, unix_time


class TopicCls(db.Model, ModelMixin):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    content = db.Column(db.String(256))
    created_time = db.Column(db.String(100))
    lastreplytime = db.Column(db.String(100))
    replycount = db.Column(db.Integer, default=0)
    views = db.Column(db.Integer, default=0)

    #
    node_id = db.Column(db.Integer, db.ForeignKey('nodes.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    replyuser_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('CommentCls', backref='topic_ref')

    def __init__(self, form):
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.created_time = unix_time()
        self.lastreplytime = self.created_time
        self.replycount = 0
        self.views = 0

    def isvalid_topic(self):
        if len(self.title) > 3 and len(self.content) > 3:
            return True
        else:
            return False

    def view_add(self):
        self.views = (self.views or 0) + 1
        self.save()

    def get_customized_comments(self, cur_user):
        user_id = cur_user.id
        comments = self.comments
        cs = []
        for c in comments:
            r = c.dict_response()
            if not CommentLike.query.filter_by(user_id=user_id, comment_id=c.id).first():
                r['islike'] = False
            else:
                r['islike'] = True
            cs.append(r)
        return cs


class CommentCls(db.Model, ModelMixin):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(256))
    created_time = db.Column(db.String(100))
    like_num = db.Column(db.Integer, default=0)
    #
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, form):
        self.content = form.get('content', '')
        self.created_time = unix_time()
        self.topic_id = int(form.get('topic_id', -1))

    def isvalid_comment(self):
        if len(self.content) > 3 and self.topic_id > 0:
            return True
        else:
            return False

    def topic_update(self):
        t = TopicCls.query.get(self.topic_id)
        t.lastreplytime = self.created_time
        t.replyuser_id = self.sender_id
        t.replycount = (t.replycount or 0) + 1
        t.save()

    def like_handle(self, comment_id, cur_user):
        form = dict(
            comment_id=comment_id,
            user_id=cur_user.id,
        )
        cl = CommentLike.query.filter_by(user_id=cur_user.id, comment_id=comment_id).first()
        if not cl:
            CommentLike(form).save()
            self.like_num += 1
            self.save()
            delta = 1
        else:
            CommentLike.delete(cl.id)
            self.like_num -= 1
            self.save()
            delta = -1

        return True, {'delta': delta}, 'like handled ok'


    def dict_response(self):
        r = dict(
            id=self.id,
            avatar=self.sender_ref.avatar,
            sender_name=self.sender_ref.username,
            receiver_name=self.receiver_ref.username,
            created_time=self.created_time,
            content=self.content,
            sender_id=self.sender_ref.id,
            like_num=self.like_num,
        )
        return r


class CommentLike(db.Model, ModelMixin):
    __tablename__ = 'commentlike'
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    created_time = db.Column(db.String(100), default=0)

    def __init__(self, form):
        self.created_time = unix_time()
        self.comment_id = form.get('comment_id')
        self.user_id = form.get('user_id')