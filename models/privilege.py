from models import db


class Privilege(db.Model):
    __tablename__ = "privilege"
    pid = db.Column(db.Integer, primary_key=True)
    privilege_name = db.Column(db.String(32), unique=True)
    operate_manga = db.Column(db.Boolean, default=False)
    operate_chapter = db.Column(db.Boolean, default=False)
    operate_quest = db.Column(db.Boolean, default=False)
    accept_quest = db.Column(db.Boolean, default=False)
    issue_invitation = db.Column(db.Boolean, default=False)
    upload_file = db.Column(db.Boolean, default=False)
    delete_file = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Privilege %r>' % self.privilege_name
