def create_manga(uid, name, cover=None):
    from models import db
    from models.user import User
    from models.manga import Manga
    import base64
    # check user privilege
    user = User.query.get(uid)
    if not user.privilege.operate_manga:
        return 1
    # create manga
    new_manga = Manga(manga_name=name, manga_cover=cover)
    db.session.add(new_manga)
    db.session.commit()
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
    quest1_code = create_quest(uid, "翻译", "ARTICLE", new_chapter.cid)
    quest2_code = create_quest(uid, "嵌字", "IMAGES", new_chapter.cid)
    return 0


def create_quest(uid, name, quest_type, cid):
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
    new_quest = Quest(quest_name=name, quest_type=quest_type, cid=cid, create_uid=uid)
    db.session.add(new_quest)
    db.session.commit()
    update_quest(new_quest)
    return 0


def manga_title(uid, new_title, mid):
    from models import db
    from models.user import User
    from models.manga import Manga
    # check user privilege
    user = User.query.get(uid)
    if not user.privilege.operate_quest:
        return 1
    # check manga existence
    manga = Manga.query.get(mid)
    if manga is None:
        return 2
    # change title
    manga.manga_name = new_title
    db.session.commit()
    update_manga(manga)
    return 0


def manga_cover(uid, new_cover, mid):
    from models import db
    from models.user import User
    from models.manga import Manga
    # check user privilege
    user = User.query.get(uid)
    if not user.privilege.operate_quest:
        return 1
    # check manga existence
    manga = Manga.query.get(mid)
    if manga is None:
        return 2
    # change title
    manga.manga_cover = new_cover
    db.session.commit()
    update_manga(manga)
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
