from . import db, ModelMixin

class TopicCls(db.Model, ModelMixin):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True)
    content = db.Column(db.String(256))
   # timestap = db.Column(db.Integer)
    #
    node_id = db.Column(db.Integer, db.ForeignKey('nodes.id'))
  #  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


    def __init__(self, form):
        self.title = form.get('title', '')
        self.content = form.get('content', '')

    def isvalid_topic(self):
        if len(self.title) > 0 and len(self.content) > 3:
            return True
        else:
            return False