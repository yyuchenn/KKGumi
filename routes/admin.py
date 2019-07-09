from flask import Blueprint, render_template,session, request, redirect, abort
from routes.user import is_login
from json import JSONEncoder

admin_bp = Blueprint('admin', __name__, static_folder='../static', template_folder='../templates', url_prefix='/admin')


@admin_bp.route('/add_manga', methods=['POST'])
@is_login
def add_manga():
    from services.content_manager import create_manga
    title = request.form["title"]
    cover = request.form["cover"]
    try:
        code = create_manga(session.get('uid'), title, cover)
    except Exception:
        code = 500
        abort(500)
    response = {'code': code}
    return JSONEncoder().encode(response)


@admin_bp.route('/add_chapter', methods=['POST'])
@is_login
def add_chapter():
    from services.content_manager import create_chapter
    title = request.form["title"]
    mid = request.form["mid"]
    try:
        code = create_chapter(session.get('uid'), title, mid)
    except Exception:
        code = 500
        abort(500)
    response = {'code': code}
    return JSONEncoder().encode(response)


@admin_bp.route('/add_quest', methods=['POST'])
@is_login
def add_quest():
    from services.content_manager import create_quest
    name = request.form["name"]
    quest_type = request["quest_type"]
    cid = request.form["cid"]
    try:
        code = create_quest(session.get('uid'), name, quest_type, cid)
    except Exception:
        code = 500
        abort(500)
    response = {'code': code}
    return JSONEncoder().encode(response)