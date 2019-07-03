from models import db


class Privilege(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    privilege_name = db.Column(db.String(32), unique=True)

    def __init__(self, gid):
        self.gid = gid

    def __repr__(self):
        return '<Privilege %r>' % self.group_name
