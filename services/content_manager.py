def create_manga(uid, name, cover):
    from models import db
    from services.user_services import get_user_by_uid
    from services.resource_manager import upload_resource, compress_image
    from models.manga import Manga
    from os.path import join
    # check user privilege
    user = get_user_by_uid(uid)
    if not user.privilege.operate_manga:
        return 1
    # create manga
    new_manga = Manga(manga_name=name)
    db.session.add(new_manga)
    db.session.commit()
    resource = upload_resource(cover, uid, '.sys/manga/'+str(new_manga.mid), True, filename='cover')
    new_manga.manga_cover_rid = resource.rid
    db.session.commit()
    compress_image(join(resource.resource_path, resource.resource_name))
    update_manga(new_manga)
    return 0


def create_chapter(uid, name, mid):
    from models import db
    from models.user import User
    from models.manga import Manga
    from models.chapter import Chapter
    # check user privilege
    user = User.query.get(uid)
    if not user.privilege.operate_chapter:
        return 1
    # check manga existence
    manga = Manga.query.get(mid)
    if manga is None:
        return 2
    # create chapter
    new_chapter = Chapter(chapter_name=name, aff_mid=mid)
    db.session.add(new_chapter)
    db.session.commit()
    update_chapter(new_chapter)
    # create two default quests
    quest1_code = create_quest(uid, "翻译", "ARTICLE", False, new_chapter.cid)
    quest2_code = create_quest(uid, "嵌字", "ARTICLE", False, new_chapter.cid)
    return 0


def create_quest(uid, name, quest_type, public_accessibility, cid):
    from models import db
    from models.user import User
    from models.chapter import Chapter
    from models.quest import Quest
    # check user privilege
    user = User.query.get(uid)
    if not user.privilege.operate_quest:
        return 1
    # check chapter existence
    chapter = Chapter.query.get(cid)
    if chapter is None:
        return 2
    # create quest
    new_quest = Quest(quest_name=name, quest_type=quest_type, cid=cid, create_uid=uid, public_access=public_accessibility)
    db.session.add(new_quest)
    db.session.commit()
    update_quest(new_quest)
    return 0


def manga_title(uid, new_title, mid):
    from models import db
    from services.user_services import get_user_by_uid
    # check user privilege
    user = get_user_by_uid(uid)
    if not user.privilege.operate_quest:
        return 1
    # check manga existence
    manga = get_manga_by_mid(mid)
    if manga is None:
        return 2
    # change title
    manga.manga_name = new_title
    db.session.commit()
    update_manga(manga)
    return 0


def manga_cover(uid, new_cover, mid):
    from models import db
    from services.user_services import get_user_by_uid
    from services.resource_manager import upload_resource, delete_resource, compress_image
    from os.path import join
    # check user privilege
    user = get_user_by_uid(uid)
    if not user.privilege.operate_quest:
        return 1
    # check manga existence
    manga = get_manga_by_mid(mid)
    if manga is None:
        return 2
    # change cover
    old_cover = manga.manga_cover
    manga.manga_cover_rid = None
    db.session.commit()
    delete_resource(old_cover, uid)
    resource = upload_resource(new_cover, uid, '.sys/manga/' + str(manga.mid), True, filename='cover')
    manga.manga_cover_rid = resource.rid
    db.session.commit()
    compress_image(join(resource.resource_path, resource.resource_name))
    update_manga(manga)
    return 0


def manga_status(uid, new_status, mid):
    from models import db
    from services.user_services import get_user_by_uid
    # check user privilege
    user = get_user_by_uid(uid)
    if not user.privilege.operate_quest:
        return 1
    # check manga existence
    manga = get_manga_by_mid(mid)
    if manga is None:
        return 2
    # check status validity
    if new_status not in ["WORKING", "HALT", "FINISHED"]:
        return 3
    manga.status = new_status
    db.session.commit()
    return 0


def get_mangas():
    from models.manga import Manga
    return Manga.query.filter_by().order_by(Manga.last_update.desc())


def get_quests(uid=None, status=None):
    from models.quest import Quest
    if status is None and uid is None:
        return Quest.query.filter_by().order_by(Quest.last_update.desc())
    if status is None:
        return Quest.query.filter_by(accept_uid=uid).order_by(Quest.last_update.desc())
    if uid is None:
        return Quest.query.filter_by(status=status).order_by(Quest.last_update.desc())
    return Quest.query.filter_by(status=status, accept_uid=uid).order_by(Quest.last_update.desc())


def get_manga_by_mid(mid):
    from models.manga import Manga
    manga = Manga.query.get(mid)
    return manga


def get_chapter_by_cid(cid):
    from models.chapter import Chapter
    chapter = Chapter.query.get(cid)
    if chapter is not None:
        manga = chapter.manga
        if manga is not None:
            return chapter, manga
    return None, None


def get_quest_by_qid(qid):
    from models.quest import Quest
    quest = Quest.query.get(qid)
    if quest is not None:
        chapter = quest.chapter
        manga = quest.chapter.manga
        if chapter is not None and manga is not None:
            return quest, chapter, manga
    return None, None, None


def update_manga(manga):
    from models import db
    manga.last_update = db.func.now()
    db.session.commit()


def update_chapter(chapter):
    from models import db
    chapter.last_update = db.func.now()
    db.session.commit()
    update_manga(chapter.manga)


def update_quest(quest):
    from models import db
    quest.last_update = db.func.now()
    db.session.commit()
    update_chapter(quest.chapter)


def chapter_mark(uid, cid, mark):
    from services.user_services import get_user_by_uid
    from models import db
    # check user privilege
    if get_user_by_uid(uid).privilege.operate_chapter is not True:
        return 1
    chapter, useless = get_chapter_by_cid(cid)
    if chapter.status == "FINISHED" and mark == "WORKING":
        chapter.status = "WORKING"
    if chapter.status == "WORKING" and mark == "FINISHED":
        chapter.status = "FINISHED"
    if chapter.status == "WORKING" and mark == "HALT":
        chapter.status = "HALT"
        # halt all non-finished quests
        from services.quest_manager import close_quest
        for quest in chapter.quests:
            if quest.status != "FINISHED":
                try:
                    code = close_quest(uid, quest.qid)
                except:
                    pass
    if chapter.status == "HALT" and mark == "WORKING":
        chapter.status = "WORKING"
        # reopen all non-finished quests
        from services.quest_manager import reopen_quest
        for quest in chapter.quests:
            if quest.status != "FINISHED":
                try:
                    code = reopen_quest(uid, quest.qid)
                except:
                    pass
    db.session.commit()
    return 0


def change_notes(uid, mid, notes):
    from models import db
    from models.user import User
    # check user privilege
    user = User.query.get(uid)
    if not user.privilege.accept_quest:
        return 1
    # check manga existence
    manga = get_manga_by_mid(mid)
    if manga is None:
        return 2
    # change notes
    manga.manga_notes = notes
    db.session.commit()
    return 0


def delete_chapter(uid, cid):
    from models import db
    from services.user_services import get_user_by_uid
    from services.quest_manager import delete_quest
    # check user privilege
    chapter, useless = get_chapter_by_cid(cid)
    user = get_user_by_uid(uid)
    if not user.privilege.operate_chapter:
        return 1
    # delete quests
    for quest in chapter.quests:
        delete_quest(uid, quest.qid)
    # delete chapter
    db.session.delete(chapter)
    db.session.commit()
    return 0
