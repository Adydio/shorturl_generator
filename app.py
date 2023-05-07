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

#主界面
@app.route('/')
def index():
    return render_template('index.html')

#生成
@app.route('/generate', methods=['POST'])
def generate():
    long_url = request.form.get('long_url')#获取表单信息
    try:
        long_url_add = URLModel(url=long_url)
        db.session.add(long_url_add)
        db.session.commit()#将长url存储进数据库
    except pymysql.Error:
        raise
    last_id = URLModel().find_id()
    encode = bases.toBase62(last_id)#将长url的id在62进制转换下与shorturl进行一一对应
    short_url = host + encode
    return render_template('index.html', short_url=short_url)

#跳转
@app.route('/<encode_id>')
def redirect_url(encode_id):
    id = bases.fromBase62(encode_id)#将短地址的后缀字符串转换为数据库对应的id
    url = URLModel().find_url(id)#找到对应长url
    return redirect(url)


if __name__ == '__main__':
    app.run(debug=True)