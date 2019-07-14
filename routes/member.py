from flask import Blueprint, render_template, session
from .user import is_login

member_bp = Blueprint('member', __name__, static_folder='../static', template_folder='../templates', url_prefix='/')


@member_bp.route('/member')
def members():
    from services.user_services import get_user_by_uid, get_users
    return render_template('members.html', user=get_user_by_uid(session.get('uid')), get_users=get_users)


@member_bp.route('/member/<uid>')
def members_check(uid):
    from services.user_services import get_user_by_uid
    from services.content_manager import get_quests
    return render_template('member_template.html', user=get_user_by_uid(session.get('uid')), member=get_user_by_uid(uid), get_quests=get_quests)
