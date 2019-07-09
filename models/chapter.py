from models import db


class Chapter(db.Model):
    __tablename__ = "chapter"
    cid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chapter_name = db.Column(db.String(64))
    aff_mid = db.Column(db.Integer, db.ForeignKey("manga.mid"))
    release_rid = db.Column(db.Integer, db.ForeignKey("resource.rid"))
    create_on = db.Column(db.TIMESTAMP, default=db.func.now())
    last_update = db.Column(db.TIMESTAMP, default=db.func.now())
    status = db.Column(db.String(32), default="WORKING")  # ["WORKING", "HALT", "FINISHED"]

    manga = db.relationship("Manga", backref=db.backref("chapters", order_by=create_on.desc()), foreign_keys="Chapter.aff_mid") # TODO: order doesn't work
    release_file = db.relationship("Resource", foreign_keys="Chapter.release_rid")

    def __repr__(self):
        return '<Chapter %r>' % self.cid
