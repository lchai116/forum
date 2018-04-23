from flask import Blueprint, render_template, redirect, url_for, request, flash, session, abort
from flask_bootstrap import Bootstrap
from models.user import UserCls
from functools import wraps
import json, random, uuid

bootstrap = Bootstrap()


def cur_user():
    uid = session.get('user_id')
    if uid is not None:
        u = UserCls.query.get(uid)
        return u
    else:
        return uid


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not cur_user():
            return redirect(url_for('auth_blue.signin'))
        return f(*args, **kwargs)
    return wrapper


# response template for ajax request
def api_response(status=False, data=None, message=''):
    r = dict(
        success=status,
        data=data,
        message=message,
    )
    return json.dumps(r)
