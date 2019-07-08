from flask import Blueprint, render_template,session, request, redirect
from routes.user import is_login
from services.content_manager import create_manga
from json import JSONEncoder

admin_bp = Blueprint('admin', __name__, static_folder='../static', template_folder='../templates', url_prefix='/admin')


@admin_bp.route('/add_manga', methods=['POST'])
@is_login
def add_manga():
    title = request.form["title"]
    cover = request.form["cover"]
    code = create_manga(session.get('uid'), title, cover)
    response = {'code': code}
    return JSONEncoder().encode(response)
