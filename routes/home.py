from flask import Blueprint, render_template, session
from .user import is_login

home_bp = Blueprint('home', __name__, static_folder='../static', template_folder='../templates', url_prefix='/')


@home_bp.route('/')
def index():
    from services.user_services import get_user_by_uid
    from services.content_manager import get_quests
    from services import statistics
    from services.content_manager import get_mangas
    return render_template('index.html', user=get_user_by_uid(session.get('uid')), get_quests=get_quests, mangas=get_mangas(), statistics=statistics)


@home_bp.route('/about')
def about():
    from services.user_services import get_user_by_uid
    return render_template('about.html', user=get_user_by_uid(session.get('uid')))


@home_bp.route('/files')
@is_login
def files():
    from services.user_services import get_user_by_uid
    return render_template('files.html', user=get_user_by_uid(session.get('uid')))
