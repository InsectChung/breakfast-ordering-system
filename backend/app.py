from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

db = SQLAlchemy()

# 定義菜單資料表模型
class MenuItem(db.Model):
    __tablename__ = 'menu_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    price = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(500))
    stock = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'image_url': self.image_url,
            'stock': self.stock
        }

# 定義訂單模型 (為了讓測試通過，這裡也補上 Order 相關定義)
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    total_amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='pending')
    
    # 關聯設定
    items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(36), db.ForeignKey('orders.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, nullable=False) # 簡化對應
    quantity = db.Column(db.Integer, nullable=False)


def create_app():
    app = Flask(__name__)
    
    # --- 關鍵修改：使用 SQLite ---
    # 這樣設定會將資料庫檔案存在 backend 資料夾下的 breakfast.db
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'breakfast.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    CORS(app)

    # 註冊藍圖 (如果你的 routes 資料夾結構還在，可以保留這段，否則先註解掉以免報錯)
    # from routes.menu import menu_bp
    # from routes.orders import orders_bp
    # app.register_blueprint(menu_bp, url_prefix='/api/v1')
    # app.register_blueprint(orders_bp, url_prefix='/api/v1')

    # 自動建立資料表
    with app.app_context():
        db.create_all()

    # 為了讓前端能動，我們暫時保留舊的路由在 app.py (若你有用 Blueprint 可移除)
    @app.route('/api/v1/menu', methods=['GET'])
    def get_menu():
        items = MenuItem.query.all()
        return jsonify([item.to_dict() for item in items])

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)