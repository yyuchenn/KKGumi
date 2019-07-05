from models import db


class Chapter(db.Model):
    __tablename__ = "chapter"
    cid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chapter_name = db.Column(db.String(64))
    aff_mid = db.Column(db.Integer, db.ForeignKey("manga.mid"))
    release_rid = db.Column(db.Integer, db.ForeignKey("resource.rid"))
    create_on = db.Column(db.TIMESTAMP, default=db.func.now())

    aff_manga = db.relationship("Manga", backref="chapter", foreign_keys="Chapter.aff_mid")
    release_file = db.relationship("Resource", foreign_keys="Chapter.release_rid")

    def __repr__(self):
        return '<Chapter %r>' % self.cid
