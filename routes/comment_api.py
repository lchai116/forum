from models.topic import TopicCls, CommentCls
from models.node import NodeCls
from . import *


main = Blueprint('commentApi_blue', __name__)
Model = CommentCls


@main.route('/comment/like', methods=['post'])
def comment_like():
    form = request.form
    comment_id = int(form.get('comment_id'))
    u = cur_user()
    comment = CommentCls.query.get(comment_id)
    if not comment:
        return api_response()
    status, data, message = comment.like_handle(comment_id, u)
    return api_response(status, data, message)



