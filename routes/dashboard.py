from flask import Blueprint, render_template, request, url_for, redirect, session
from .user import is_login
from services import user_services
from json import JSONEncoder

dashboard_bp = Blueprint('dashboard', __name__, static_folder='../static', template_folder='../templates', url_prefix='/dashboard')


@dashboard_bp.route('')
@is_login
def dashboard():
    return render_template('dashboard.html')


@dashboard_bp.route('/issue_icode', methods=['GET', 'POST']) # TODO: remove GET method in the future
@is_login
def issue_icode():
    privilege = 2 # TODO: For now, only issue privilege 2
    code, i_code = user_services.issue_invitation(session['uid'], privilege)
    response = {'code': code, 'i_code': i_code}
    print(i_code)
    return JSONEncoder().encode(response)