from flask import Blueprint, render_template, request, url_for, redirect, session
from .user import is_login
from services import user_services
from json import JSONEncoder

dashboard_bp = Blueprint('dashboard', __name__, static_folder='../static', template_folder='../templates', url_prefix='/dashboard')


@dashboard_bp.route('')
@is_login
def dashboard():
    from services.user_services import get_user_by_uid
    return render_template('dashboard/dashboard.html', user=get_user_by_uid(session['uid']))


@dashboard_bp.route('/icode', methods=['GET', 'POST'])
@is_login
def icode():
    if request.method == 'GET':
        from services.user_services import get_user_by_uid
        return render_template('dashboard/invitation.html', user=get_user_by_uid(session['uid']))
    privilege = 2 # TODO: For now, only issue privilege 2
    code, i_code = user_services.issue_invitation(session['uid'], privilege)
    response = {'code': code, 'i_code': i_code}
    print(i_code)
    return JSONEncoder().encode(response)


@dashboard_bp.route('/profile')
@is_login
def profile():
    from services.user_services import get_user_by_uid
    return render_template('dashboard/profile.html', user=get_user_by_uid(session['uid']))


@dashboard_bp.route('/quest')
@is_login
def quest():
    from services.user_services import get_user_by_uid
    return render_template('dashboard/quest.html', user=get_user_by_uid(session['uid']))


@dashboard_bp.route('/content')
@is_login
def content():
    from services.user_services import get_user_by_uid
    return render_template('dashboard/content.html', user=get_user_by_uid(session['uid']))
