from models import db


class Resource(db.Model):
    __tablename__ = "resource"
    fid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_name = db.Column(db.String(256))
    file_path = db.Column(db.String(256))
    file_ref = db.Column(db.String(256))
    uploader_uid = db.Column(db.Integer, db.ForeignKey("user.uid"))
    create_on = db.Column(db.TIMESTAMP, default=db.func.now())

    uploader = db.relationship("User", backref="upload_file", foreign_keys="Resource.uploader_uid")

    def __repr__(self):
        return '<Resource %r>' % self.fid
