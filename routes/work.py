from flask import Blueprint, render_template

work_bp = Blueprint('work', __name__, static_folder='../static', template_folder='../templates', url_prefix='/work')


# TODO
