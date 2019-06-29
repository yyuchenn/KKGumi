from flask import Blueprint, render_template

home_bp = Blueprint('home', __name__, static_folder='../static', template_folder='../templates', url_prefix='/')


@home_bp.route('/')
def index():
    return render_template('index.html')


@home_bp.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('login.html')


@home_bp.route('/logout')
def logout():
    # TODO
    pass


@home_bp.route('/signup')
def signup():
    # TODO
    pass
