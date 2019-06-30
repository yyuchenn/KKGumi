from flask import Blueprint, render_template
from .user import is_login

dashboard_bp = Blueprint('dashboard', __name__, static_folder='../static', template_folder='../templates', url_prefix='/dashboard')


@dashboard_bp.route('')
@is_login
def dashboard():
    return render_template('dashboard.html')