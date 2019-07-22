from conf import RESOURCE_FOLDER


def upload_file(uid, folder, file):
    from services.resource_manager import upload_resource, get_resource_url
    res = upload_resource(file, uid, folder, False)
    return get_resource_url(res)


def folder_ls(folder):
    from services.resource_manager import get_resource_by_uri
    from os import listdir,path
    full_path = path.abspath(path.join(RESOURCE_FOLDER,folder))
    everything = listdir(full_path)
    files = []
    folders = []
    for thing in everything:
        if path.isfile(path.join(full_path,thing)):
            files.append(thing)
        else:
            folders.append(thing)
    files_res = []
    for file in files:
        res = get_resource_by_uri(path.join('/resource', folder, file))
        if res is not None:
            files_res.append(res)
    return files_res, folders
