from app import create_app
from models import MenuItem, db

def seed_data():
    app = create_app()
    with app.app_context():
        print("正在初始化資料庫種子資料...")
        
        # 定義要新增的測試資料
        items_data = [
            {
                "name": "經典蛋餅",
                "description": "外皮酥脆，內餡軟嫩的傳統口味蛋餅。",
                "price": 30.0,
                "image_url": "https://placehold.co/300x200?text=Egg+Pancake",
                "category": "main",
                "stock": 50
            },
            {
                "name": "冰美式",
                "description": "選用精選咖啡豆，口感清爽回甘。",
                "price": 45.0,
                "image_url": "https://placehold.co/300x200?text=Iced+Americano",
                "category": "drink",
                "stock": 100
            },
            {
                "name": "三明治",
                "description": "新鮮吐司搭配火腿與荷包蛋，營養滿分。",
                "price": 35.0,
                "image_url": "https://placehold.co/300x200?text=Sandwich",
                "category": "main",
                "stock": 40
            }
        ]

        for data in items_data:
            # 檢查是否已存在，避免重複新增
            if not MenuItem.query.filter_by(name=data['name']).first():
                item = MenuItem(**data)
                db.session.add(item)
                print(f"已新增: {data['name']}")
        
        db.session.commit()
        print("資料庫初始化完成！")

if __name__ == "__main__":
    seed_data()