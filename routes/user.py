from flask import Blueprint, request, render_template, session, redirect, url_for, make_response
from services import user_services
from functools import wraps
from urllib.parse import parse_qs
from json import JSONEncoder

user_bp = Blueprint('user', __name__, static_folder='../static', template_folder='../templates', url_prefix='/')


def is_login(func):
    @wraps(func)
    def check_login(*args, **kwargs):
        if session.get('uid') is not None and session.get('uid') != -1:  # uid == -1 for no login
            return func(*args, **kwargs)
        else:
            return redirect('/login?callback=' + url_for('.' + func.__name__, **kwargs))
    return check_login


@user_bp.route('/login', methods=['POST', 'GET'])
def login():
    callback = parse_qs(request.query_string.decode('utf8')).get(b'callback')
    if callback is None:
        callback = '/dashboard'  # default callback url
    else:
        callback = callback[0]
    if session.get('uid') is not None and session.get('uid') != -1:
        return redirect(callback)
    # login process
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('user')
        password = request.form.get('pwd')
        response = {}
        try:
            code = user_services.login_service(username, password)
            if code == 0:
                session['uid'] = user_services.get_uid_by_username(username)
                session.permanent = True
                response['code'] = 0  # successful
            else:
                response['code'] = code  # failed
        except AssertionError as e:
            import sys
            from datetime import datetime
            sys.stderr.write("%s - - %s\n" % (str(datetime.now()), e))
            response['code'] = 500  # fatal error
        return JSONEncoder().encode(response)


@user_bp.route('/logout')
def logout():
    session['uid'] = -1
    return redirect('/')


@user_bp.route('/signup', methods=['POST', 'GET'])
def signup():
    # setup callback url
    try:
        callback = parse_qs(request.query_string).get(b'callback')
    except:
        callback = None
    if callback is None:
        callback = '/dashboard'  # default callback url
    else:
        callback = callback[0]
    # setup i_code
    i_code = parse_qs(request.query_string).get(b'i_code')
    # callback directly if already login
    if session.get('uid') is not None and session.get('uid') != -1:
        return redirect(callback)
    # signup process
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        username = request.form.get('user')
        password = request.form.get('pwd')
        response = {}
        try:
            code = user_services.signup_service(username, password, i_code)
            if code == 0:
                session['uid'] = user_services.get_uid_by_username(username)
                response['code'] = 0  # successful
            else:
                response['code'] = code  # failed
        except AssertionError as e:
            import sys
            from datetime import datetime
            sys.stderr.write("%s - - %s\n" % (str(datetime.now()), e))
            response['code'] = 500  # fatal error
        return JSONEncoder().encode(response)


@user_bp.route('/dashboard/change_nickname', methods=['POST'])
@is_login
def change_nickname_route():
    from services.user_services import change_nickname
    uid = session.get('uid')
    new_nickname = request.form.get('new_nickname')
    code = change_nickname(uid, new_nickname)
    response = {'code': code}
    return JSONEncoder().encode(response)


@user_bp.route('/dashboard/change_introduction', methods=['POST'])
@is_login
def change_introduction_route():
    from services.user_services import change_introduction
    uid = session.get('uid')
    new_introduction = request.form.get('new_introduction')
    code = change_introduction(uid, new_introduction)
    response = {'code': code}
    return JSONEncoder().encode(response)


@user_bp.route('/dashboard/change_password', methods=['POST'])
@is_login
def change_password_route():
    from services.user_services import change_password
    uid = session.get('uid')
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    try:
        code = change_password(uid, old_password, new_password)
    except AssertionError as e:
        code = 500
    response = {'code': code}
    return JSONEncoder().encode(response)
