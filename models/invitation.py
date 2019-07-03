from models import db


class Invitation(db.Model):
    __tablename__ = "invitation"
    i_code = db.Column(db.String(64), primary_key=True)
    inviter_uid = db.Column(db.Integer, db.ForeignKey("user.uid"))

    inviter = db.relationship("User", backref="invitation_codes")

    def __repr__(self):
        return '<Invitation %r>' % self.i_code
