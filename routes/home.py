from flask import Blueprint, render_template

home_bp = Blueprint('home', __name__, static_folder='../static', template_folder='../templates', url_prefix='/')


@home_bp.route('/')
def index():
    return render_template('index.html')
