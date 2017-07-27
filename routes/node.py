from models.node import NodeCls
from models.user import UserCls
from models.topic import TopicCls
from . import *
#from flask import Blueprint


main = Blueprint('node_blue', __name__)


@main.route('/')
def index():
    ns = NodeCls.query.all()
    u = None #current_user()
    return render_template('node_index.html', node_list=ns, user=u)


#@main.route('/<int:id>')
#def show(id):
#    n = NodeCls.query.get(id)
#    ns = NodeCls.query.all()
#    topic_list = n.topics
#    return render_template('node.html', nodes=ns, topics=topic_list)


@main.route('/<int:id>')
def show(id):
    n = NodeCls.query.get(id)
    ns = NodeCls.query.all()
    topic_list = n.topics
    page = request.args.get('p', 1, type=int)
    pagination = TopicCls.query.filter_by(node_id=id).paginate(page, per_page=6)
    ts = pagination.items
    u = cur_user()
    return render_template('node.html', node=n, node_list=ns, topics=ts, pagination=pagination, user=u)



@main.route('/add', methods=['post'])
def new():
    form = request.form
    n = NodeCls(form)
    n.save()
    print url_for('.index')
    return redirect(url_for('.index'))


@main.route('/edit/<int:id>')
def edit(id):
    return render_template('node_edit.html', nodeid=id)


@main.route('/update/<int:id>', methods=['post'])
def update(id):
    n = NodeCls.query.get(id)
    n.node_name = request.form.get('node_name', '')
    n.save()
    return redirect(url_for('.index'))


@main.route('/delete/<int:id>')
def remove(id):
    n = NodeCls.query.get(id)
    n.delete()
    return redirect(url_for('.index'))
