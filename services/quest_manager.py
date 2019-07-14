def accept_quest(agent_uid, accept_uid, qid):
    from models.user import User
    from models.quest import Quest
    from models import db
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
