from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///breakfast.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    CORS(app)
    
    with app.app_context():
        # 這裡會創建資料庫表
        db.create_all()
        
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)