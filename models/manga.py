from models import db


class Manga(db.Model):
    __tablename__ = "manga"
    mid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    manga_name = db.Column(db.String(64))
    manga_cover = db.Column(db.LargeBinary)
    manga_notes = db.Column(db.String(10000))

    def __repr__(self):
        return '<Manga %r>' % self.mid
