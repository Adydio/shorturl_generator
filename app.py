from flask import Flask, render_template, request, redirect
import config
from models import URLModel
from exts import db
import pymysql
from bases import Bases
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
bases = Bases()
host = 'http://127.0.0.1:5000/'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/gen_short_url', methods=['POST'])
def gen_short_url():
    long_url = request.form.get('long_url')
    try:
        long_url_add = URLModel(url=long_url)
        db.session.add(long_url_add)
        db.session.commit()
    except pymysql.Error:
        raise
    last_id = URLModel().find_id()
    encode = bases.toBase62(last_id)
    short_url = host + encode
    return render_template('index.html', short_url=short_url)


@app.route('/<encode_id>')
def redirect_url(encode_id):
    id = bases.fromBase62(encode_id)
    url = URLModel().find_url(id)
    return redirect(url)


if __name__ == '__main__':
    app.run(debug=True)