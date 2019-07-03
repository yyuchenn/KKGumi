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
            return redirect('/login?callback=' + url_for('.' + func.__name__))
    return check_login


@user_bp.route('/login', methods=['POST', 'GET'])
def login():
    callback = parse_qs(request.query_string).get(b'callback')
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
            if user_services.is_matched_password(username, password):
                session['uid'] = user_services.get_uid_by_username(username)
                response['code'] = 0  # successful
            else:
                response['code'] = 1  # password does not match
        except AssertionError as e:
            import sys
            from datetime import datetime
            sys.stderr.write("%s - - %s\n" % (str(datetime.now()), e))
            response['code'] = 2  # fatal error
        return JSONEncoder().encode(response)


@user_bp.route('/logout')
def logout():
    session['uid'] = -1
    return redirect('/')


@user_bp.route('/signup', methods=['POST', 'GET'])
def signup():
    # setup callback url
    callback = parse_qs(request.query_string).get(b'callback')
    if callback is None:
        callback = '/dashboard'  # default callback url
    else:
        callback = callback[0]
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
            if user_services.signup_service(username, password):
                session['uid'] = user_services.get_uid_by_username(username)
                response['code'] = 0  # successful
            else:
                response['code'] = 1  # bad request
        except AssertionError as e:
            import sys
            from datetime import datetime
            sys.stderr.write("%s - - %s\n" % (str(datetime.now()), e))
            response['code'] = 2  # fatal error
        return JSONEncoder().encode(response)
