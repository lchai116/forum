from models.topic import TopicCls
from models.node import NodeCls
from . import *


main = Blueprint('topic_blue', __name__)
Model = TopicCls
# csrftoken_map = {}


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
        return redirect(url_for('node_blue.show'))
    m.view_add()
    u = cur_user()
    token = ''
    if u:
        token = str(uuid.uuid4())
        csrftoken_map[token] = u.id
    topic = m.get_customized_topic(u)
    cs = m.get_customized_comments(u)
    return render_template('topic.html', topic=topic, comments=cs, cur_user=u, csrftoken=token)


@main.route('/edit/<int:id>')
@login_required
def edit(id):
    return render_template('topic_edit.html', topicid=id)


@main.route('/update/<int:id>', methods=['post'])
@login_required
def update(id):
    m = Model.query.get(id)
    m.node_name = request.form.get('content', '')
    m.save()
    return redirect(url_for('.index'))


@main.route('/delete/<int:id>', methods=['post'])
@login_required
def remove(id):
    token = request.form.get('csrftoken')
    u = cur_user()
    if csrftoken_map.get(token, '') == u.id and Model.isvalid_delete(u, id):
        csrftoken_map.pop(token)
        Model.delete(id)
        return redirect(url_for('node_blue.show', id=1))
    else:
        abort(403)