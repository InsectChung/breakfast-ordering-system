import pytest
import sys
import os

# 將 backend 目錄加入 sys.path，確保能正確匯入 app 和 models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from models import User

@pytest.fixture
def app():
    """建立測試用的 Flask App 與記憶體資料庫"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def test_user_password_hashing(app):
    """測試 User 模型的密碼雜湊與驗證功能"""
    with app.app_context():
        user = User(name='Test User', email='test@example.com')
        password = 'secure_password_123'
        
        # 設定密碼
        user.set_password(password)
        
        # 1. 驗證密碼欄位已被加密 (不是明碼)
        assert user.password_hash != password
        
        # 2. 驗證 check_password 方法能否正確運作
        assert user.check_password(password) is True
        assert user.check_password('wrong_password') is False

def test_user_to_dict(app):
    """測試 to_dict 方法是否正確隱藏敏感資訊"""
    with app.app_context():
        user = User(name='Test User', email='test@example.com')
        user.set_password('secret')
        
        data = user.to_dict()
        
        # 3. 驗證 password_hash 不在回傳的字典中
        assert 'password_hash' not in data
        assert 'password' not in data
        assert data['email'] == 'test@example.com'
        assert data['name'] == 'Test User'