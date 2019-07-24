from flask import Blueprint, render_template,session, request, redirect, abort
from routes.user import is_login
from json import JSONEncoder

admin_bp = Blueprint('admin', __name__, static_folder='../static', template_folder='../templates', url_prefix='/admin')


@admin_bp.route('/add_manga', methods=['POST'])
@is_login
def add_manga():
    from services.content_manager import create_manga
    title = request.form["title"]
    cover = request.files["cover"]
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
    quest_type = request.form["quest_type"]
    public_accessibility = int(request.form["public_accessibility"])
    cid = request.form["cid"]
    try:
        code = create_quest(session.get('uid'), name, quest_type, public_accessibility, cid)
    except Exception:
        code = 500
        abort(500)
    response = {'code': code}
    return JSONEncoder().encode(response)


@admin_bp.route('/change_manga_title', methods=['POST'])
@is_login
def change_manga_title():
    from services.content_manager import manga_title
    title = request.form["new_title"]
    mid = request.form['mid']
    try:
        code = manga_title(session.get('uid'), title, mid)
    except Exception:
        code = 500
        abort(500)
    response = {'code': code}
    return JSONEncoder().encode(response)


@admin_bp.route('/change_manga_cover', methods=['POST'])
@is_login
def change_manga_cover():
    from services.content_manager import manga_cover
    cover = request.files["new_cover"]
    mid = request.form['mid']
    try:
        code = manga_cover(session.get('uid'), cover, mid)
    except Exception:
        code = 500
        abort(500)
    response = {'code': code}
    return JSONEncoder().encode(response)


@admin_bp.route('/change_manga_status', methods=['POST'])
@is_login
def change_manga_status():
    from services.content_manager import manga_status
    status = request.form["new_status"]
    mid = request.form['mid']
    try:
        code = manga_status(session.get('uid'), status, mid)
    except Exception:
        code = 500
        abort(500)
    response = {'code': code}
    return JSONEncoder().encode(response)


@admin_bp.route('/chapter_mark', methods=['POST'])
@is_login
def chapter_mark():
    from services.content_manager import chapter_mark
    uid = session.get('uid')
    cid = request.form.get('cid')
    mark = request.form.get('mark')
    code = chapter_mark(uid, cid, mark)
    return JSONEncoder().encode({'code': code})


@admin_bp.route('/change_quest_accessibility', methods=['POST'])
@is_login
def change_quest_accessibility():
    from services.quest_manager import change_quest_accessibility
    qid = request.form["qid"]
    new_accessibility = int(request.form["new_accessibility"])
    code = change_quest_accessibility(session.get('uid'), qid, new_accessibility)
    response = {'code': code}
    return JSONEncoder().encode(response)


@admin_bp.route('/delete_quest', methods=['POST'])
@is_login
def delete_quest():
    from services.quest_manager import delete_quest
    qid = request.form["qid"]
    code = delete_quest(session.get('uid'), qid)
    response = {'code': code}
    return JSONEncoder().encode(response)


@admin_bp.route('/delete_chapter', methods=['POST'])
@is_login
def delete_chapter():
    from services.content_manager import delete_chapter
    cid = request.form["cid"]
    code = delete_chapter(session.get('uid'), cid)
    response = {'code': code}
    return JSONEncoder().encode(response)
