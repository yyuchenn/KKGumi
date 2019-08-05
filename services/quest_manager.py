def accept_quest(agent_uid, accept_uid, qid):
    from services.content_manager import update_quest
    from services.resource_manager import get_all_resources_under_path, change_resource_uploader
    from services.user_services import get_user_by_uid, update_user
    from models import db
    agent_uid = str(agent_uid)
    # check agent privilege
    if agent_uid != accept_uid:
        if not get_user_by_uid(agent_uid).privilege.operate_quest:
            return 2
    # check user privilege
    if not get_user_by_uid(accept_uid).privilege.accept_quest:
        return 1
    quest = get_quest_by_qid(qid)
    # check quest availability
    if quest.status != "HIRING":
        return 3
    # TODO: solve simultaneous problem
    quest.accept_uid = accept_uid
    quest.accept_on = db.func.now()
    update_quest(quest)
    quest.status = "WORKING"
    db.session.commit()
    update_user(accept_uid)
    # assign uploader to resources if exist
    if quest.resource is not None:
        resources = get_all_resources_under_path(".sys/quest/" + str(qid))
        for resource in resources:
            try:
                change_resource_uploader(resource, accept_uid)
            except:
                pass
    return 0


def finish_quest(uid, qid):
    from services.user_services import get_user_by_uid, update_user
    from models import db
    # check user privilege
    quest = get_quest_by_qid(qid)
    if quest.accept_uid != uid and not get_user_by_uid(uid).privilege.operate_quest:
        return 1
    # mark it finish
    quest.complete_on = db.func.now()
    quest.status = "FINISHED"
    db.session.commit()
    update_user(uid)
    # chain opener
    quests = quest.chapter.quests
    if quest.quest_type == "TRANSLATION" or quest.quest_type == "PROOFREADING":
        if quest.quest_type == "TRANSLATION":
            unfinished_translation = []
            proofreading = []
            typesetting = []
            for q in quests:
                if q.quest_type == "TRANSLATION" and (q.status == "WORKING" or q.status == "HIRING"):
                    unfinished_translation.append(q)
                elif q.quest_type == "PROOFREADING":
                    proofreading.append(q)
                elif q.quest_type == "TYPESETTING":
                    typesetting.append(q)
            if len(unfinished_translation) == 0:
                if len(proofreading) > 0:
                    for q in proofreading:
                        if q.status == "CLOSED":
                            reopen_quest(uid, q.qid, force=True)
                else:
                    for q in typesetting:
                        if q.status == "CLOSED":
                            reopen_quest(uid, q.qid, force=True)
        if quest.quest_type == "PROOFREADING":
            unfinished_translation = []
            unfinished_proofreading = []
            typesetting = []
            for q in quests:
                if q.quest_type == "TRANSLATION" and (q.status == "WORKING" or q.status == "HIRING"):
                    unfinished_translation.append(q)
                elif q.quest_type == "PROOFREADING" and (q.status == "WORKING" or q.status == "HIRING"):
                    unfinished_proofreading.append(q)
                elif q.quest_type == "TYPESETTING":
                    typesetting.append(q)
            if len(unfinished_translation) == 0 and len(unfinished_proofreading) == 0:
                for q in typesetting:
                    if q.status == "CLOSED":
                        reopen_quest(uid, q.qid, force=True)
    # auto finishing chapter
    for q in quests:
        if q.status != "FINISHED":
            return 0
    from services.content_manager import chapter_mark
    chapter_mark(uid, quest.chapter.cid, "FINISHED", force=True)
    return 0


def update_article(uid, qid, article):
    from models.quest import Quest
    from models import db
    from services.resource_manager import update_resource
    from services.user_services import update_user
    quest = Quest.query.get(qid)
    # check quest status
    if quest.status != "WORKING":
        return 1
    # check user privilege
    if quest.accept_uid != uid:
        return 2
    # if the resource dose not exist, then create one
    if quest.resource_rid is None:
        register_article(uid, quest, "article.html")
    # update article
    if not update_resource(quest.resource, article, uid):
        return 500
    # update metadata and user data
    quest.last_update = db.func.now()
    db.session.commit()
    update_user(uid)
    return 0


def register_article(uid, quest, filename):
    from services.resource_manager import create_resource
    from models import db
    public_access = quest.public_access
    rid = create_resource(filename, uid, ".sys/quest/" + str(quest.qid), public_access).rid
    quest.resource_rid = rid
    db.session.commit()


def register_content(uid, quest, files):
    from services.resource_manager import upload_resource, get_resource_url
    from models import db
    public_access = quest.public_access
    urls = {}
    for filetag in files:
        resource = upload_resource(files[filetag], uid, ".sys/quest/" + str(quest.qid), public_access)
        db.session.commit()
        urls[filetag] = get_resource_url(resource)
    return urls


def fetch_original(uid, qid, source_qid, to_article):
    from models.quest import Quest
    from services.resource_manager import copy_resource, get_resource_by_uri, create_resource
    from os.path import join
    from models import db
    print(uid, qid, source_qid, type(to_article))
    quest = Quest.query.get(qid)
    source_quest = Quest.query.get(source_qid)
    # check quest status
    if quest.status != "WORKING":
        return 1
    # check user privilege
    if quest.accept_uid != uid:
        return 2
    # check target resource existence
    if source_quest.resource is None:
        return 3
    # fetch original
    # source_article_uri = join("/resource/.sys/quest/", str(source_qid), "article.html")
    target_original_uri = join("/resource/.sys/quest/", str(qid), "original.html")
    target_article_uri = join("/resource/.sys/quest/", str(qid), "article.html")
    res_source = source_quest.resource
    res_original = get_resource_by_uri(target_original_uri)
    if res_original is None:
        res_original = create_resource("original.html", uid, join(".sys/quest", str(qid)), False)
    res_target = get_resource_by_uri(target_article_uri)
    if res_target is None:
        res_target = create_resource("article.html", uid, join(".sys/quest", str(qid)), False)
        quest.resource_rid = res_target.rid
        db.session.commit()
    copy_resource(res_original, res_source)
    if to_article:
        copy_resource(res_target, res_source)
    return 0


def get_quest_by_qid(qid):
    from models.quest import Quest
    return Quest.query.get(qid)


def close_quest(uid, qid):
    from models import db
    from services.user_services import get_user_by_uid
    # check user privilege
    quest = get_quest_by_qid(qid)
    user = get_user_by_uid(uid)
    if not user.privilege.operate_quest:
        return 1
    # mark it close
    quest.complete_on = db.func.now()
    quest.status = "CLOSED"
    db.session.commit()
    return 0


def reopen_quest(uid, qid, force=False):
    from models import db
    from services.user_services import get_user_by_uid
    # check user privilege
    quest = get_quest_by_qid(qid)
    user = get_user_by_uid(uid)
    if force is not True and not user.privilege.operate_quest:
        return 1
    # mark it open
    quest.complete_on = db.func.now()
    if quest.accept_uid is not None:
        quest.status = "WORKING"
    else:
        quest.status = "HIRING"
    db.session.commit()
    return 0


def transfer_quest(uid, qid):
    from models import db
    from services.user_services import get_user_by_uid
    from services.resource_manager import delete_resource, change_resource_uploader, get_all_resources_under_path
    # check user privilege
    quest = get_quest_by_qid(qid)
    user = get_user_by_uid(uid)
    if not user.privilege.operate_quest:
        return 1
    # update quest
    quest.status = "HIRING"
    quest.accept_uid = None
    res = quest.resource
    # quest.resource_rid = None
    db.session.commit()
    if res is not None:
        # delete_resource(res, res.uploader_uid)
        # change the owner of all files under the quest folder to nobody
        resources = get_all_resources_under_path(".sys/quest/" + str(qid))
        for resource in resources:
            try:
                change_resource_uploader(resource, None)
            except:
                pass
    return 0


def change_quest_accessibility(uid, qid, new_accessibility):
    from models import db
    from services.user_services import get_user_by_uid
    from services.resource_manager import get_all_resources_under_path, change_resource_accessibility
    # check user privilege
    quest = get_quest_by_qid(qid)
    user = get_user_by_uid(uid)
    if not user.privilege.operate_quest:
        return 1
    # check quest status
    if quest.status != "FINISHED" and quest.status != "CLOSED":
        return 2
    # change resources accessibility
    resources = get_all_resources_under_path('.sys/quest/' + qid)
    for res in resources:
        change_resource_accessibility(res, uid, new_accessibility)
    # change quest accessibility
    quest.public_access = new_accessibility
    db.session.commit()
    return 0


def delete_quest(uid, qid):
    from models import db
    from services.user_services import get_user_by_uid
    from services.resource_manager import get_all_resources_under_path, delete_resource
    # check user privilege
    quest = get_quest_by_qid(qid)
    user = get_user_by_uid(uid)
    if not user.privilege.operate_quest:
        return 1
    # delete all resources under the quest file
    try:
        resources = get_all_resources_under_path(".sys/quest/" + qid)
        for res in resources:
            delete_resource(res, uid)
    except:
        pass
    db.session.delete(quest)
    db.session.commit()
    return 0
