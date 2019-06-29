from flask import Blueprint, render_template

dashboard_bp = Blueprint('dashboard', __name__, static_folder='../static', template_folder='../templates', url_prefix='/dashboard')


@dashboard_bp.route('/')
def dashboard():
    return render_template('dashboard.html')