from models.topic import TopicCls, CommentCls
from models.node import NodeCls
from . import *


main = Blueprint('comment_blue', __name__)
Model = CommentCls


@main.route('/add', methods=['post'])
@login_required
def new():
    form = request.form
    m = Model(form)
    if m.isvalid_comment():
        m.sender_id = cur_user().id
        m.save()
        m.topic_reply_update()
        return redirect(url_for('topic_blue.show', id=m.topic_id))
    else:
        abort(403)
