from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
# 設定資料庫位置 (這裡使用 SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///breakfast.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

# ==========================================
# 👇 這裡是重點：必須要有這個 Class 定義 👇
# ==========================================
class MenuItem(db.Model):
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
# ==========================================

# 建立資料庫 (如果資料表不存在的話)
with app.app_context():
    db.create_all()

# --- 你的 API 路由 (Routes) 會寫在下面 ---
@app.route('/api/v1/menu', methods=['GET'])
def get_menu():
    items = MenuItem.query.all()
    return jsonify([item.to_dict() for item in items])

if __name__ == '__main__':
    app.run(debug=True)