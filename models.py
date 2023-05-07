from exts import db


class URLModel(db.Model):
    #数据表信息设置
    __tablename__ = "urls"
    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    url = db.Column(db.String(10000), nullable=False)
    #通过id找到对应url
    def find_url(self, id):
        url = URLModel.query.filter(URLModel.id == id).first().url
        return url
    #获取当前最后一个数据（即刚刚存储的数据）的id
    def find_id(self):
        return URLModel.query.order_by(URLModel.id.desc()).first().id