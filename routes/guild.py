from flask import Blueprint, render_template, session, request
from .user import is_login
from json import JSONEncoder

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


@guild_bp.route('/update_article', methods=['POST'])
@is_login
def update_article():
    from services.quest_manager import update_article
    from json import JSONEncoder
    uid = session.get('uid')
    qid = request.form.get('qid')
    article = request.form.get('article')
    code = update_article(uid, qid, article)
    return JSONEncoder().encode({'code': code})


@guild_bp.route('/upload_file', methods=['POST'])
@is_login
def guild_upload_file():
    from services.quest_manager import get_quest_by_qid, register_content
    #print(request.form)
    uid = session.get('uid')
    qid = request.form.get('qid')
    urls = register_content(uid, get_quest_by_qid(qid), request.files)
    response = {'code': 0, 'urls': urls}
    return JSONEncoder().encode(response)
