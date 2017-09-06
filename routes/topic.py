from models.topic import TopicCls
from models.node import NodeCls
from . import *


main = Blueprint('topic_blue', __name__)
Model = TopicCls
csrftoken_map = {}


@main.route('/add', methods=['post'])
@login_required
def new():
    form = request.form
    m = Model(form)
    if m.isvalid_topic():
        m.node_id = int(form.get('node_id', -1))
        m.user_id = cur_user().id
        m.replyuser_id = m.user_id
        m.save()
        return redirect(url_for('topic_blue.show', id=m.id))
    else:
        return '<h1>hello</h1>'


@main.route('/<int:id>')
def show(id):
    m = Model.query.get(id)
    if not m:
        return redirect(url_for('node_blue.show', id=1))
    m.view_add()
    ns = NodeCls.query.all()
    u = cur_user()
    token = ''
    if u:
        token = str(uuid.uuid4())
        csrftoken_map[token] = u.id
    cs = m.get_customized_comments(u)
    return render_template('topic.html', topic=m, comments=cs, cur_user=u, csrftoken=token)


@main.route('/edit/<int:id>')
def edit(id):
    return render_template('topic_edit.html', topicid=id)


@main.route('/update/<int:id>', methods=['post'])
def update(id):
    m = Model.query.get(id)
    m.node_name = request.form.get('content', '')
    m.save()
    return redirect(url_for('.index'))


@main.route('/delete/<int:id>', methods=['post'])
def remove(id):
    token = request.form.get('csrftoken')
    u = cur_user()
    if csrftoken_map.get(token, '') == u.id:
        Model.delete(id)
        return redirect(url_for('node_blue.show', id=1))
    else:
        abort(403)