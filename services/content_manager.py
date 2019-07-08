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
    print(cover)
    #cover = cover.encode()
    new_manga = Manga(manga_name=name, manga_cover=cover)
    db.session.add(new_manga)
    db.session.commit()
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
    new_chapter = Chapter(chapter_name=name, aff_mid=mid, aff_manga=manga)
    db.session.add(new_chapter)
    db.session.commit()
    return 0


def get_mangas():
    from models.manga import Manga
    return Manga.query.all()


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
