from models import db


class Site(db.Model):
    __tablename__ = "site"
    key = db.Column(db.String(64), primary_key=True)
    value = db.Column(db.String(64))

    def __repr__(self):
        return '<Site %s>' % self.key
