from flask import Blueprint, render_template

user_bp = Blueprint('user', __name__, static_folder='../static', template_folder='../templates', url_prefix='/user')


# TODO
