from models import db


class Resource(db.Model):
    __tablename__ = "resource"
    rid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resource_name = db.Column(db.String(256))
    resource_path = db.Column(db.String(256))
    public_access = db.Column(db.Boolean, default=False)
    uploader_uid = db.Column(db.Integer, db.ForeignKey("user.uid"))
    inline_blob = db.Column(db.BLOB(length=65536))
    create_on = db.Column(db.TIMESTAMP, default=db.func.now())

    uploader = db.relationship("User", backref="upload_file", foreign_keys="Resource.uploader_uid")

    def __repr__(self):
        from os.path import join
        return join("/resource/", self.resource_path, self.resource_name)
