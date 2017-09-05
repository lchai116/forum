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


@main.route('/')
def index():
    ms = Model.query.all()
    return render_template('topic_index.html', topics_list=ms)


@main.route('/add', methods=['post'])
@login_required
def new():
    form = request.form
    m = Model(form)
    if m.isvalid_comment():
        m.sender_id = cur_user().id
        m.receiver_id = int(form.get('receiver_id', -1))
        m.save()
        m.topic_update()
        return redirect(url_for('topic_blue.show', id=m.topic_id))
    else:
        return '<h1>hello</h1>'


@main.route('/<int:id>')
def show(id):
    m = Model.query.get(id)
    ns = NodeCls.query.all()
    u = cur_user()
    return render_template('topic.html', topic=m, node_list=ns, cur_user=u)


@main.route('/edit/<int:id>')
def edit(id):
    return render_template('topic_edit.html', topicid=id)


@main.route('/update/<int:id>', methods=['post'])
def update(id):
    m = Model.query.get(id)
    m.node_name = request.form.get('content', '')
    m.save()
    return redirect(url_for('.index'))


@main.route('/delete/<int:id>')
def remove(id):
    m = Model.query.get(id)
    m.delete()
    return redirect(url_for('.index'))
