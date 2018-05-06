from models.user import UserCls
from models.topic import TopicCls, CommentCls, TopicCollection
from . import *


main = Blueprint('user_blue', __name__)
upload_dir = '/static/uploads/'


@main.route('/profile/<username>')
def profile(username):
    u = UserCls.query.filter_by(username=username).first()
    if u:
        cur_u = cur_user()
        tpc_rel = TopicCls.query.join(CommentCls, CommentCls.topic_id==TopicCls.id)\
                .filter(CommentCls.sender_id==u.id)\
                .order_by(CommentCls.created_time.desc()).limit(5)#.filter(CommentCls.sender_id==u.id)
        tpc_create = TopicCls.query.filter_by(user_id=u.id).order_by(TopicCls.created_time.desc()).limit(5)

        return render_template('user/profile.html', user=u, topics_created=tpc_create,
                                topics_related=tpc_rel, cur_user=cur_u)
    else:
        abort(404)


def valid_img_upload(filename):
    suffix = filename.split('.')[-1]
    return suffix.lower() in ['png', 'jpg', 'gif']


@main.route('/addimg', methods=['post'])
def add_img():
    u = cur_user()
    f = request.files.get('avatar')
    if f and valid_img_upload(f.filename):
        filename = str(uuid.uuid4())
        path = upload_dir + filename + '.' + f.filename.split('.')[-1]
        f.save(path[1:])
        u.avatar = path
        u.save()
    return redirect(url_for('user_blue.profile', username=u.username))


@main.route('/profile/<username>/topics')
def user_topics(username):
    u = UserCls.query.filter_by(username=username).first()
    if u:
        cur_u = cur_user()
        page = request.args.get('p', 1, type=int)
        pagination = TopicCls.query.filter_by(user_id=u.id)\
                    .order_by(TopicCls.created_time.desc()).paginate(page, per_page=8)
        user_topics = pagination.items

        return render_template('user/usertopics.html', user=u, topics_created=user_topics,
                               pagination=pagination, cur_user=cur_u)
    else:
        abort(404)


@main.route('/profile/<username>/favorite')
@login_required
def user_favorite(username):
    u = UserCls.query.filter_by(username=username).first()
    cur_u = cur_user()
    if u.id == cur_u.id:
        page = request.args.get('p', 1, type=int)
        pagination = TopicCls.query.join(TopicCollection, TopicCollection.topic_id == TopicCls.id) \
            .filter(TopicCollection.user_id == u.id).order_by(TopicCollection.created_time.desc()) \
            .paginate(page, per_page=8)

        favorite = pagination.items

        return render_template('user/userfavorite.html', user=u, favorite=favorite,
                               pagination=pagination, cur_user=cur_u)
    else:
        abort(403)


@main.route('/profile/<username>/replies')
def user_replied_topics(username):
    u = UserCls.query.filter_by(username=username).first()
    if u:
        cur_u = cur_user()
        page = request.args.get('p', 1, type=int)
        pagination = TopicCls.query.join(CommentCls, CommentCls.topic_id == TopicCls.id) \
            .filter(CommentCls.sender_id == u.id) \
            .order_by(CommentCls.created_time.desc()).paginate(page, per_page=8)

        tpc_rel = pagination.items

        return render_template('user/user_replied_topics.html', user=u, topics_replied=tpc_rel,
                               pagination=pagination, cur_user=cur_u)
    else:
        abort(403)