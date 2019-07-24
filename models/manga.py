from models import db


class Manga(db.Model):
    __tablename__ = "manga"
    mid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    manga_name = db.Column(db.String(64))
    manga_cover_rid = db.Column(db.Integer, db.ForeignKey("resource.rid"))
    manga_notes = db.Column(db.String(10000))
    create_on = db.Column(db.TIMESTAMP, default=db.func.now())
    last_update = db.Column(db.TIMESTAMP, default=db.func.now())
    status = db.Column(db.String(32), default="WORKING")  # ["WORKING", "HALT", "FINISHED"] TODO: make it into enum type

    manga_cover = db.relationship("Resource", foreign_keys="Manga.manga_cover_rid")

    def __repr__(self):
        return '<Manga %r>' % self.mid
