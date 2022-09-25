from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.db import db
from app.models import User

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


# API's

