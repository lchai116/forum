from models.topic import TopicCls
from models.node import NodeCls
from . import *


main = Blueprint('backend_blue', __name__)
Model = NodeCls
csrftoken_map = {}


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
    print url_for('backend_blue.index')
    return redirect(url_for('backend_blue.index'))


@main.route('/delete/<int:id>', methods=['post'])
def remove(id):
    token = request.form.get('csrftoken')
    u = cur_user()
    if csrftoken_map.get(token, '') == u.id:
        Model.delete(id)
        return redirect(url_for('backend_blue.index'))
    else:
        abort(403)