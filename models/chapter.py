from models import db


class Chapter(db.Model):
    __tablename__ = "chapter"
    cid = db.Column(db.Integer, primary_key=True)
    chapter_name = db.Column(db.String(64))

    def __init__(self, cid, chapter_name):
        self.cid = cid
        self.chapter_name = chapter_name

    def __repr__(self):
        return '<Chapter %r>' % self.cid
