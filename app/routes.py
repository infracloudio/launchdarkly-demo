from flask import render_template
from flask import Blueprint

core = Blueprint("core", __name__)

@core.route('/')
def index():
    return render_template('index.html')


@core.route('/fashion')
def fashion():
    return render_template('shop-fashion.html')

@core.route('/electronics')
def electronics():
    return render_template('shop-electronic.html')

@core.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

