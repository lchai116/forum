from models.user import UserCls
from . import *

main = Blueprint('user_blue', __name__)


@main.route('/login', methods=['post', 'get'])
def signin():
    if request.method == 'POST':
        form = request.form
        u = UserCls(form)
        if u.validate_login():
            u_db = UserCls.query.filter_by(username=u.username).first()
            session['user_id'] = u_db.id
            return redirect(url_for('node_blue.show', id=1))
        else:
            flash('Incorrect username or password!')
            return redirect(url_for('.signin'))
    else:
        return render_template('user/login.html')


@main.route('/signup',methods=['post', 'get'])
def signup():
    if request.method == 'POST':
        form = request.form
        u = UserCls(form)
        if u.validate_register():
            u.save()
            u_db = UserCls.query.filter_by(username=u.username).first()
            session['user_id'] = u_db.id
            return redirect(url_for('node_blue.show', id=1))
        else:
            flash('Username exists or length shorter than 4 chars!')
            return redirect(url_for('.signup'))
    else:
        return render_template('user/signup.html')


@main.route('/signout')
@login_required
def signout():
    session.pop('user_id', None)
    return redirect(url_for('node_blue.show', id=1))