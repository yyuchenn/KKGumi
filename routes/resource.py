from flask import Blueprint, render_template, session, send_from_directory, abort, request
from .user import is_login
from json import JSONEncoder

resource_bp = Blueprint('resource', __name__, static_folder='../static', template_folder='../templates', url_prefix='/')


@resource_bp.route('/resource/<path:filepath>')
def resource_distribute(filepath):
    from services.resource_manager import retrieve_info
    dirname, basename, accessibility = retrieve_info(filepath)
    if accessibility is False and (session.get('uid') is None or session.get('uid') == -1):
        abort(403)
    return send_from_directory(dirname, basename)


@resource_bp.route('/pan/')
@is_login
def pan_index():
    from services.user_services import get_user_by_uid
    from services.file_manager import folder_ls
    from os.path import join
    uid = session.get('uid')
    try:
        files_res, folders = folder_ls('')
        return render_template('pan.html', user=get_user_by_uid(uid), files_res=files_res, folders=folders, cur='', join=join)
    except FileNotFoundError:
        abort(404)


@resource_bp.route('/pan/<path:path>')
@is_login
def pan_dir(path):
    from services.user_services import get_user_by_uid
    from services.file_manager import folder_ls
    from os.path import join
    uid = session.get('uid')
    try:
        files_res, folders = folder_ls(path)
        return render_template('pan.html', user=get_user_by_uid(uid), files_res=files_res, folders=folders, cur=path, join=join)
    except FileNotFoundError:
        abort(404)


@resource_bp.route('/upload_file', methods=['POST'])
@is_login
def upload_file():
    from services.file_manager import upload_file
    uid = session.get('uid')
    folder = request.form.get('folder')
    url = upload_file(uid, folder, request.files['file'])
    response = {'code': 0, 'url': url}
    return JSONEncoder().encode(response)


@resource_bp.route('/delete_file', methods=['POST'])
@is_login
def delete_file():
    from services.resource_manager import delete_resource, get_resource_by_uri
    uid = session.get('uid')
    uri = request.form.get('uri')
    print(uri)
    code = delete_resource(get_resource_by_uri(uri), uid)
    response = {'code': code}
    return JSONEncoder().encode(response)
