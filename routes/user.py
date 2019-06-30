from flask import Blueprint, request, render_template, session, redirect, url_for, make_response
from services.user_services import is_matched_password, get_uid_by_username
from functools import wraps
from urllib.parse import parse_qs
from json import JSONEncoder

user_bp = Blueprint('user', __name__, static_folder='../static', template_folder='../templates', url_prefix='/')


def is_login(func):
    @wraps(func)
    def check_login(*args, **kwargs):
        if session.get('uid') != -1:  # uid == -1 for no login
            return func(*args, **kwargs)
        else:
            return redirect('/login?callback=' + url_for('.' + func.__name__))
    return check_login


@user_bp.route('/login', methods=['POST', 'GET'])
def login():
    # setup callback url
    callback = parse_qs(request.query_string).get(b'callback')
    if callback is None:
        callback = '/dashboard'  # default callback url
    else:
        callback = callback[0]
    if session.get('uid') != -1:
        return redirect(callback)
    # login process
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('user')
        password = request.form.get('pwd')
        try:
            if is_matched_password(username, password):
                session['uid'] = get_uid_by_username(username)
                return redirect(callback)
            return JSONEncoder().encode({'code': 1})
        except:
            return redirect('/login')


@user_bp.route('/logout')
def logout():
    session['uid'] = -1
    return redirect('/')


@user_bp.route('/signup')
def signup():
    # TODO
    pass
