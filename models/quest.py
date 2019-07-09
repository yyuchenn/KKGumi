from models import db


class Quest(db.Model):
    __tablename__ = "quest"
    qid = db.Column(db.Integer, primary_key=True)
    quest_name = db.Column(db.String(64))
    quest_type = db.Column(db.String(64))  # see `conf.QUEST_TYPES` for possible values
    cid = db.Column(db.Integer, db.ForeignKey("chapter.cid"))
    create_on = db.Column(db.TIMESTAMP, default=db.func.now())
    create_uid = db.Column(db.Integer, db.ForeignKey("user.uid"))
    accept_uid = db.Column(db.Integer, db.ForeignKey("user.uid"))
    accept_on = db.Column(db.TIMESTAMP)
    complete_on = db.Column(db.TIMESTAMP)
    resource_rid = db.Column(db.Integer, db.ForeignKey("resource.rid"))
    last_update = db.Column(db.TIMESTAMP, default=db.func.now())
    status = db.Column(db.String(32), default="HIRING")  # ["HIRING", "WORKING", "CLOSED", "FINISHED"]

    chapter = db.relationship("Chapter", backref="quests", foreign_keys="Quest.cid")
    create_by = db.relationship("User", backref="create_quests", foreign_keys="Quest.create_uid")
    accept_by = db.relationship("User", backref="quests", foreign_keys="Quest.accept_uid")
    resource = db.relationship("Resource", backref="quest", foreign_keys="Quest.resource_rid")

    def __repr__(self):
        return '<Quest %r>' % self.qid