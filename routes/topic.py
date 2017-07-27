from models.topic import TopicCls
from models.node import NodeCls
from . import *


main = Blueprint('topic_blue', __name__)
Model = TopicCls


@main.route('/')
def index():
    ms = Model.query.all()
    return render_template('topic_index.html', topics_list=ms)


@main.route('/add', methods=['post'])
def new():
    form = request.form
    m = Model(form)
    if m.isvalid_topic():
        m.node_id = int(form.get('node_id', -1))
        m.save()
        print url_for('.index')
        flash('Title is required and content must be longer than 8 characters')
        return redirect(url_for('node_blue.show', id=m.node_id))
    else:
        flash('Title is required and content must be longer than 8 characters')
        return '<h1>hello</h1>'

@main.route('/<int:id>')
def show(id):
    m = Model.query.get(id)
    ns = NodeCls.query.all()
    return render_template('topic.html', topic=m, node_list=ns)


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
