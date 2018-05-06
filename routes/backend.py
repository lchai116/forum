from models.node import NodeCls
from models.topic import CommentCls
from . import *


main = Blueprint('backend_blue', __name__)
# csrftoken_map = {}


def admin_required():
    u = cur_user()
    if not u or not u.is_admin():
        abort(403)


main.before_request(admin_required)


@main.route('/')
def index():
    ns = NodeCls.query.all()
    u = cur_user()
    token = str(uuid.uuid4())
    csrftoken_map[token] = u.id
    return render_template('user/backend.html', node_list=ns, csrftoken=token)


@main.route('/add', methods=['post'])
def new():
    form = request.form
    n = NodeCls(form)
    n.save()
    return redirect(url_for('backend_blue.index'))


@main.route('/node/delete/<int:id>', methods=['post'])
def node_remove(id):
    token = request.form.get('csrftoken')
    u = cur_user()
    if csrftoken_map.get(token, '') == u.id:
        NodeCls.delete(id)
        return redirect(url_for('backend_blue.index'))
    else:
        abort(403)


@main.route('/comment/delete/<int:id>', methods=['post'])
def comment_remove(id):
    token = request.form.get('csrftoken')
    u = cur_user()
    if csrftoken_map.get(token, '') == u.id:
        c = CommentCls.query.get(id)
        CommentCls.delete(id)
        return redirect(url_for('topic_blue.show', id=c.topic_id))
    else:
        abort(403)