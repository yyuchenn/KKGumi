from models import db


class Quest(db.Model):
    __tablename__ = "quest"
    qid = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<Chapter %r>' % self.qid