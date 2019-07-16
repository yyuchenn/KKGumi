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
    rid = create_resource(filename, uid, "quest/" + str(quest.qid))
    quest.resource_rid = rid
    db.session.commit()


def register_content(uid, qid, file):
    pass
