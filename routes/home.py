from flask import Blueprint, render_template, session

home_bp = Blueprint('home', __name__, static_folder='../static', template_folder='../templates', url_prefix='/')


@home_bp.route('/')
def index():
    if session.get('uid') is not None:
        from services.user_services import get_user_by_uid
        return render_template('index.html', user=get_user_by_uid(session.get('uid')))
    else:
        return render_template('index.html')
