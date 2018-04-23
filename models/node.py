from . import db, ModelMixin


class NodeCls(db.Model, ModelMixin):
    __tablename__ = 'nodes'
    id = db.Column(db.Integer, primary_key=True)
    node_name = db.Column(db.String(64), unique=True)
    # relationship with topic
    topics = db.relationship('TopicCls', backref='node_ref', lazy='dynamic')

    def __init__(self, form):
        self.node_name = form.get('node_name', '')


