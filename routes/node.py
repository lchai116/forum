from models.node import NodeCls
from models.user import UserCls
from models.topic import TopicCls
from . import *


main = Blueprint('node_blue', __name__)


@main.route('/')
@main.route('/<int:id>')
def show(id=1):
    n = NodeCls.query.get(id)
    ns = NodeCls.query.all()
    page = request.args.get('p', 1, type=int)
    pagination = TopicCls.query.filter_by(node_id=id) \
        .order_by(TopicCls.lastreplytime.desc(), TopicCls.created_time.desc()) \
        .paginate(page, per_page=6)
    ts = pagination.items
    u = cur_user()
    return render_template('node.html', node=n, node_list=ns, topics=ts, pagination=pagination, cur_user=u)
