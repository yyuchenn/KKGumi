def upload_resource(file, user, path):
    pass


def create_resource(filename, uid, path):
    from models.resource import Resource
    from models import db
    from os.path import exists
    from os import makedirs
    secure_filename(filename)
    if not exists("resource/"+path):
        makedirs("resource/"+path)
    new_file = open("resource/"+path+"/"+filename, "w")
    new_resource = Resource(resource_name=filename, resource_path=path, uploader_uid=uid)
    db.session.add(new_resource)
    db.session.commit()
    return new_resource.rid


def check_resource(res):
    file = open("resource/" + res.resource_path + "/" + res.resource_name, "r")
    return file.read()


def update_resource(res, content, uid):
    # check user privilege
    if res.uploader_uid != uid:
        return False
    file = open("resource/"+res.resource_path+"/"+res.resource_name, "w")
    file.write(content)
    file.close()
    return True


def delete_resource(res, uid):
    pass


def secure_filename(filename):
    from re import search
    assert search("^\.", filename) is None
    assert search("/", filename) is None
