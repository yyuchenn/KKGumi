from flask import Blueprint, render_template, session, request
from .user import is_login

guild_bp = Blueprint('guild', __name__, static_folder='../static', template_folder='../templates', url_prefix='/guild')


@guild_bp.route('/accept_quest', methods=['POST'])
@is_login
def accept_quest():
    from services.quest_manager import accept_quest
    from json import JSONEncoder
    agent_uid = session.get('uid')
    accept_uid = request.form.get('accept_uid')
    qid = request.form.get('qid')
    code = accept_quest(agent_uid, accept_uid, qid)
    return JSONEncoder().encode({'code': code})
