from models.user import UserCls
from . import *


main = Blueprint('auth_blue', __name__)


@main.route('/signin', methods=['post', 'get'])
def signin():
    if request.method == 'POST':
        form = request.form
        u = UserCls(form)
        if u.validate_login():
            u_db = UserCls.query.filter_by(username=u.username).first()
            session['user_id'] = u_db.id
            r = {
                'success': True,
                'redirect_url': url_for('node_blue.show', id=1),
            }
            return json.dumps(r)
        else:
            return json.dumps({'success': False})
    else:
        return render_template('auth/signin.html')


@main.route('/signup',methods=['post', 'get'])
def signup():
    if request.method == 'POST':
        form = request.form
        u = UserCls(form)
        if u.validate_register():
            u.get_avatar()
            u.get_created_time()
            u.save()
            u_db = UserCls.query.filter_by(username=u.username).first()
            session['user_id'] = u_db.id
            r = {
                'success': True,
                'redirect_url': url_for('node_blue.show', id=1),
            }
            return json.dumps(r)
        else:
            return json.dumps({'success': False})
    else:
        return render_template('auth/signup.html')


@main.route('/signout')
@login_required
def signout():
    session.pop('user_id', None)
    return redirect(url_for('node_blue.show', id=1))
