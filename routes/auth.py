from models.user import UserCls
from . import *


main = Blueprint('auth_blue', __name__)


@main.route('/signin1', methods=['post', 'get'])
def signin1():
    if request.method == 'POST':
        form = request.form
        u = UserCls(form)
        if u.validate_login():
            u_db = UserCls.query.filter_by(username=u.username).first()
            print u
            print u_db.query
            session['user_id'] = u_db.id
            return redirect(url_for('node_blue.show', id=1))
        else:
            flash('Incorrect username or password!')
            return redirect(url_for('.signin'))
    else:
        return render_template('auth/signin.html')


@main.route('/signin', methods=['post', 'get'])
def signin():
    if request.method == 'POST':
        form = request.form
        u = UserCls(form)
        if u.validate_login():
            u_db = UserCls.query.filter_by(username=u.username).first()
            print u
            print u_db.query
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


@main.route('/signup1',methods=['post', 'get'])
def signup1():
    if request.method == 'POST':
        form = request.form
        u = UserCls(form)
        if u.validate_register():
            u.get_avatar()
            u.get_created_time()
            u.save()
            u_db = UserCls.query.filter_by(username=u.username).first()
            session['user_id'] = u_db.id
            return redirect(url_for('node_blue.show', id=1))
        else:
            flash('Username exists or length shorter than 4 chars!')
            return redirect(url_for('.signup'))
    else:
        return render_template('auth/signup.html')


@main.route('/signout')
@login_required
def signout():
    session.pop('user_id', None)
    return redirect(url_for('node_blue.show', id=1))


@main.route('/')
def index():
    return render_template('index.html')