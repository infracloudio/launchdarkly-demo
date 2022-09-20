from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/fashion')
def fashion():
    return render_template('shop-fashion.html')

@app.route('/electronics')
def electronics():
    return render_template('shop-electronic.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

