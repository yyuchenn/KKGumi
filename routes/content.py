from flask import Blueprint, render_template,session, abort
from services.content_manager import get_manga_by_mid, get_chapter_by_cid, get_quest_by_qid

work_bp = Blueprint('content', __name__, static_folder='../static', template_folder='../templates', url_prefix='/')


@work_bp.route('/manga')
def manga():
    from services.user_services import get_user_by_uid
    from services.content_manager import get_mangas
    return render_template('manga.html', user=get_user_by_uid(session.get('uid')), mangas=get_mangas())


@work_bp.route('/manga/<mid>')
def manga_check(mid):
    manga = get_manga_by_mid(mid)
    if manga is None:
        abort(404)
    from services.user_services import get_user_by_uid
    return render_template('manga_template.html', user=get_user_by_uid(session.get('uid')), manga=manga)


@work_bp.route('/chapter/<cid>')
def chapter_check(cid):
    chapter, manga = get_chapter_by_cid(cid)
    if chapter is None:
        abort(404)
    from services.user_services import get_user_by_uid
    return render_template('chapter_template.html', user=get_user_by_uid(session.get('uid')), chapter=chapter, manga=manga)



@work_bp.route('/quest/<qid>')
def quest_check(qid):
    quest, chapter, manga = get_quest_by_qid(qid)
    if quest is None:
        abort(404)
    from services.user_services import get_user_by_uid
    return render_template('quest_template.html', user=get_user_by_uid(session.get('uid')), quest=quest,)
