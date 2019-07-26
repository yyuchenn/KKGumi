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


@guild_bp.route('/finish_quest', methods=['POST'])
@is_login
def finish_quest():
    from services.quest_manager import finish_quest
    uid = session.get('uid')
    qid = request.form.get('qid')
    code = finish_quest(uid, qid)
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
    uid = session.get('uid')
    qid = request.form.get('qid')
    urls = register_content(uid, get_quest_by_qid(qid), request.files)
    response = {'code': 0, 'urls': urls}
    return JSONEncoder().encode(response)


@guild_bp.route('/fetch_original', methods=['POST'])
@is_login
def fetch_original():
    from services.quest_manager import fetch_original
    uid = session.get('uid')
    qid = request.form.get('my_qid')
    target_qid = request.form.get('target_qid')
    to_article = request.form.get('to_article')
    if to_article == 'true':
        to_article = True
    else:
        to_article = False
    code = fetch_original(uid, qid, target_qid, to_article)
    response = {'code': code}
    return JSONEncoder().encode(response)


@guild_bp.route('/close_quest', methods=['POST'])
@is_login
def close_quest():
    from services.quest_manager import close_quest
    uid = session.get('uid')
    qid = request.form.get('qid')
    code = close_quest(uid, qid)
    return JSONEncoder().encode({'code': code})


@guild_bp.route('/reopen_quest', methods=['POST'])
@is_login
def reopen_quest():
    from services.quest_manager import reopen_quest
    uid = session.get('uid')
    qid = request.form.get('qid')
    code = reopen_quest(uid, qid)
    return JSONEncoder().encode({'code': code})


@guild_bp.route('/transfer_quest', methods=['POST'])
@is_login
def transfer_quest():
    from services.quest_manager import transfer_quest
    uid = session.get('uid')
    qid = request.form.get('qid')
    code = transfer_quest(uid, qid)
    return JSONEncoder().encode({'code': code})


@guild_bp.route('/change_notes', methods=['POST'])
@is_login
def change_notes():
    from services.content_manager import change_notes
    uid = session.get('uid')
    notes = request.form.get('notes')
    mid = request.form.get('mid')
    code = change_notes(uid, mid, notes)
    return JSONEncoder().encode({'code': code})
