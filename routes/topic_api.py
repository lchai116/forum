from models.topic import TopicCls, CommentCls
from models.node import NodeCls
from . import *


main = Blueprint('topicApi_blue', __name__)


@main.route('/favor', methods=['post'])
def topic_favor():
    form = request.form
    topic_id = form.get('topic_id', -1, type=int)
    u = cur_user()
    topic = TopicCls.query.get(topic_id)
    if not topic or not u:
        return api_response()
    status, data, message = topic.favor_handle(topic_id, u)
    return api_response(status, data, message)


@main.route('/comment/like', methods=['post'])
def comment_like():
    form = request.form
    comment_id = form.get('comment_id', -1, type=int)
    u = cur_user()
    comment = CommentCls.query.get(comment_id)
    if not comment or not u:
        return api_response()
    status, data, message = comment.like_handle(comment_id, u)
    return api_response(status, data, message)



