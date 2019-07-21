def accept_quest(agent_uid, accept_uid, qid):
    from models.user import User
    from models.quest import Quest
    from models import db
    agent_uid = str(agent_uid)
    # check agent privilege
    if agent_uid != accept_uid:
        if not User.query.get(agent_uid).privilege.operate_quest:
            return 2
    # check user privilege
    if not User.query.get(accept_uid).privilege.accept_quest:
        return 1
    quest = Quest.query.get(qid)
    # check quest availability
    if quest.status != "HIRING":
        return 3
    # TODO: solve simultaneous problem
    quest.accept_uid = accept_uid
    quest.accept_on = db.func.now()
    quest.last_update = db.func.now()
    quest.status = "WORKING"
    db.session.commit()
    User.query.get(accept_uid).last_active = db.func.now()
    db.session.commit()
    return 0


def finish_quest(uid, qid):
    from models import db
    # check user privilege
    quest = get_quest_by_qid(qid)
    if quest.accept_uid != uid:
        return 1
    # mark it finish
    quest.complete_on = db.func.now()
    quest.status = "FINISHED"
    db.session.commit()
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
    rid = create_resource(filename, uid, "quest/" + str(quest.qid), public_access).rid
    quest.resource_rid = rid
    db.session.commit()


def register_content(uid, quest, files):
    from services.resource_manager import upload_resource, get_resource_url
    from models import db
    public_access = quest.public_access
    urls = {}
    for filetag in files:
        resource = upload_resource(files[filetag], uid, "quest/" + str(quest.qid), public_access)
        db.session.commit()
        urls[filetag] = get_resource_url(resource)
    return urls


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


def reopen_quest(uid, qid):
    from models import db
    from services.user_services import get_user_by_uid
    # check user privilege
    quest = get_quest_by_qid(qid)
    user = get_user_by_uid(uid)
    if not user.privilege.operate_quest:
        return 1
    # mark it close
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
    from services.resource_manager import delete_resource
    # check user privilege
    quest = get_quest_by_qid(qid)
    user = get_user_by_uid(uid)
    if not user.privilege.operate_quest:
        return 1
    # update quest
    quest.status = "HIRING"
    quest.accept_uid = None
    res = quest.resource
    quest.resource_rid = None
    db.session.commit()
    if res is not None:
        delete_resource(res, res.uploader_uid)
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
    resources = get_all_resources_under_path('quest/' + qid)
    for res in resources:
        change_resource_accessibility(res, uid, new_accessibility)
    # change quest accessibility
    quest.public_access = new_accessibility
    db.session.commit()
    return 0
