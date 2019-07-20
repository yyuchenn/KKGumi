from conf import RESOURCE_FOLDER


def upload_resource(file, uid, filepath):
    from models.resource import Resource
    from services.user_services import get_user_by_uid
    from models import db
    from os import path
    from os import makedirs
    secure_filename(file.filename)
    # check user privilege
    if get_user_by_uid(uid).privilege.upload_file is False:
        return None
    if not path.exists(RESOURCE_FOLDER + filepath):
        makedirs(RESOURCE_FOLDER + filepath)
    filename = file.filename
    # filename clash resolve
    if path.exists(path.join(RESOURCE_FOLDER + filepath, file.filename)):
        ext = '.' + filename.split('.')[-1]
        name = filename[:len(filename)-len(ext)]
        count = 1
        while path.exists(path.join(RESOURCE_FOLDER + filepath, name + '(' + str(count) + ')' + ext)):
            count += 1
        filename = name + '(' + str(count) + ')' + ext
    # save file
    file.save(path.join(RESOURCE_FOLDER + filepath, filename))
    # update database
    new_resource = Resource(resource_name=filename, resource_path=filepath, uploader_uid=uid)
    db.session.add(new_resource)
    db.session.commit()
    return new_resource


def create_resource(filename, uid, filepath):
    from models.resource import Resource
    from services.user_services import get_user_by_uid
    from models import db
    from os import path
    from os import makedirs
    secure_filename(filename)
    # check user privilege
    if get_user_by_uid(uid).privilege.upload_file is False:
        return None
    if not path.exists(RESOURCE_FOLDER + filepath):
        makedirs(RESOURCE_FOLDER + filepath)
    new_file = open(path.join(RESOURCE_FOLDER + filepath, filename), "w")
    new_resource = Resource(resource_name=filename, resource_path=filepath, uploader_uid=uid)
    db.session.add(new_resource)
    db.session.commit()
    return new_resource


def update_resource(res, content, uid):
    from os import path
    # check user privilege
    if res.uploader_uid != uid:
        return False
    file = open(path.join(RESOURCE_FOLDER + res.resource_path, res.resource_name), "w")
    file.write(content)
    file.close()
    return True


def delete_resource(res, uid):
    from models import db
    from services.user_services import get_user_by_uid
    from os import path, remove
    # check user privilege
    if res.uploader_uid != uid and get_user_by_uid(uid).privilege.delete_file is False:
        return 1
    filepath = path.abspath(RESOURCE_FOLDER + res.resource_path + "/" + res.resource_name)
    remove(filepath)
    db.session.delete(res)
    db.session.commit()
    return 0


def secure_filename(filename):
    from re import search
    assert search("^\.", filename) is None
    assert search("/", filename) is None


def retrieve_info(filepath):
    from conf import RESOURCE_FOLDER
    from models.resource import Resource
    from os import path
    abspath = path.abspath(RESOURCE_FOLDER + filepath)
    basename = path.basename(abspath)
    dirname = path.dirname(abspath)
    resource_path = path.dirname(filepath)
    res = Resource.query.filter_by(resource_path=resource_path, resource_name=basename)
    accessibility = True
    if res.count() != 0 and res[0].public_access is False:
        accessibility = False
    return dirname, basename, accessibility


def get_resource_url(res):
    return "/resource/" + res.resource_path + "/" + res.resource_name


def get_resource_by_uri(url):
    from models.resource import Resource
    from os import path
    try:
        basename = path.basename(url)
        dir = path.dirname(url).split('/')
        assert dir[0] == '' and dir[1] == 'resource'
        dirname = '/'.join(dir[2:])
        res = Resource.query.filter_by(resource_path=dirname, resource_name=basename)[0]
        return res
    except:
        return None
