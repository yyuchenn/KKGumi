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


@resource_bp.route('/pan/<path:path>')
def pan_folder(path):
    return "绝赞开发中~"


@resource_bp.route('/upload_file', methods=['POST'])
def upload_file():
    pass