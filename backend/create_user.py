from app import create_app
from models import db, User

app = create_app()

with app.app_context():
    # 檢查是否已經有用戶
    existing_user = User.query.first()

    if existing_user:
        print(f"使用者已存在，您的 User ID 是: {existing_user.user_id}")
    else:
        # 建立一個測試用戶
        new_user = User(
            email="test@example.com",
            name="測試用戶",
            phone="0912345678",
            role="customer",
            address="台北市信義區"
        )
        # 設定密碼 (使用 models.py 中定義的 set_password)
        new_user.set_password("password123")

        db.session.add(new_user)
        db.session.commit()

        print("成功建立測試用戶！")
        print(f"您的 User ID 是: {new_user.user_id}")