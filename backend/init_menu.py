# 檔案名稱: init_menu.py
from app import app, db, MenuItem

# 20 項早餐店熱門餐點資料 (含豐富飲料區)
menu_data = [
    # --- 主餐類 ---
    {
        "name": "招牌豬肉蛋堡",
        "description": "多汁豬肉排配上荷包蛋，早餐店經典首選。",
        "price": 45,
        "image_url": "https://images.unsplash.com/photo-1603064750555-408eec4115d7?w=500&auto=format&fit=crop&q=60",
        "stock": 50
    },
    {
        "name": "香煎培根蛋吐司",
        "description": "酥脆培根加上現煎嫩蛋，搭配特製美乃滋。",
        "price": 40,
        "image_url": "https://images.unsplash.com/photo-1525351484163-7529414395d8?w=500&auto=format&fit=crop&q=60",
        "stock": 50
    },
    {
        "name": "原味酥皮蛋餅",
        "description": "外皮金黃酥脆，口感層次豐富。",
        "price": 35,
        "image_url": "https://images.unsplash.com/photo-1605634676166-51e18a99496a?w=500&auto=format&fit=crop&q=60",
        "stock": 40
    },
    {
        "name": "起司薯餅蛋餅",
        "description": "濃郁起司包裹酥脆薯餅，罪惡感十足的美味。",
        "price": 55,
        "image_url": "https://plus.unsplash.com/premium_photo-1663852297267-827c73e7529e?w=500&auto=format&fit=crop&q=60",
        "stock": 30
    },
    {
        "name": "咔啦雞腿堡 (辣味)",
        "description": "現炸酥脆雞腿排，香辣過癮。",
        "price": 75,
        "image_url": "https://images.unsplash.com/photo-1619250907537-8b010b968595?w=500&auto=format&fit=crop&q=60",
        "stock": 20
    },
    {
        "name": "黑胡椒鐵板麵 (含蛋)",
        "description": "香辣黑胡椒醬汁吸附麵條，附上一顆荷包蛋。",
        "price": 65,
        "image_url": "https://images.unsplash.com/photo-1612929633738-8fe44f7ec841?w=500&auto=format&fit=crop&q=60",
        "stock": 40
    },
    {
        "name": "港式蘿蔔糕 (2片)",
        "description": "表皮煎至焦香，內裡軟嫩，沾醬油膏絕配。",
        "price": 35,
        "image_url": "https://images.unsplash.com/photo-1609123849363-2f04e1f74810?w=500&auto=format&fit=crop&q=60",
        "stock": 40
    },
    {
        "name": "火腿蛋三明治",
        "description": "新鮮火腿片搭配小黃瓜與蛋，營養均衡。",
        "price": 35,
        "image_url": "https://images.unsplash.com/photo-1553909489-cd47e35f4f81?w=500&auto=format&fit=crop&q=60",
        "stock": 50
    },
    {
        "name": "花生厚片吐司",
        "description": "抹上濃郁顆粒花生醬，烘烤至金黃香酥。",
        "price": 30,
        "image_url": "https://images.unsplash.com/photo-1550504933-4f94b150c262?w=500&auto=format&fit=crop&q=60",
        "stock": 60
    },
    {
        "name": "高麗菜煎餃 (5顆)",
        "description": "底部焦脆，內餡飽滿多汁。",
        "price": 35,
        "image_url": "https://images.unsplash.com/photo-1507755359288-294966e31db5?w=500&auto=format&fit=crop&q=60",
        "stock": 40
    },
    
    # --- 點心類 ---
    {
        "name": "麥克雞塊 (5塊)",
        "description": "金黃酥脆，大人小孩都愛的小點心。",
        "price": 45,
        "image_url": "https://images.unsplash.com/photo-1562967914-608f82629710?w=500&auto=format&fit=crop&q=60",
        "stock": 60
    },
    {
        "name": "黃金脆薯條",
        "description": "現炸馬鈴薯條，外酥內軟。",
        "price": 35,
        "image_url": "https://images.unsplash.com/photo-1573080496987-a199f8cd4054?w=500&auto=format&fit=crop&q=60",
        "stock": 50
    },
    {
        "name": "小熱狗 (3條)",
        "description": "早餐店必點經典小食。",
        "price": 20,
        "image_url": "https://images.unsplash.com/photo-1627054249767-17254552b9fb?w=500&auto=format&fit=crop&q=60",
        "stock": 80
    },

    # --- 飲料區 (擴充) ---
    {
        "name": "古早味紅茶 (大)",
        "description": "傳統決明子風味紅茶，清涼解渴。",
        "price": 25,
        "image_url": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=500&auto=format&fit=crop&q=60",
        "stock": 100
    },
    {
        "name": "招牌奶茶 (大)",
        "description": "完美比例調配，濃郁奶香不膩口。",
        "price": 30,
        "image_url": "https://images.unsplash.com/photo-1558160074-4d7d8bdf4256?w=500&auto=format&fit=crop&q=60",
        "stock": 100
    },
    {
        "name": "鮮奶茶 (大)",
        "description": "加入高品質鮮乳，口感滑順健康。",
        "price": 45,
        "image_url": "https://images.unsplash.com/photo-1571328003758-4a392120563d?w=500&auto=format&fit=crop&q=60",
        "stock": 80
    },
    {
        "name": "非基改豆漿 (大)",
        "description": "每日新鮮現磨，濃醇黃豆香。",
        "price": 25,
        "image_url": "https://images.unsplash.com/photo-1600329623832-c5df1d471549?w=500&auto=format&fit=crop&q=60",
        "stock": 60
    },
    {
        "name": "無糖豆漿 (大)",
        "description": "健康無負擔，健身族首選。",
        "price": 25,
        "image_url": "https://images.unsplash.com/photo-1563227812-0ea4c22e6cc8?w=500&auto=format&fit=crop&q=60",
        "stock": 60
    },
    {
        "name": "研磨美式咖啡",
        "description": "現磨咖啡豆，香氣濃郁提神醒腦。",
        "price": 45,
        "image_url": "https://images.unsplash.com/photo-1497935586351-b67a49e012bf?w=500&auto=format&fit=crop&q=60",
        "stock": 50
    },
    {
        "name": "玉米濃湯",
        "description": "香濃滑順，滿滿的玉米粒與火腿丁。",
        "price": 35,
        "image_url": "https://images.unsplash.com/photo-1547592166-23acbe3b624b?w=500&auto=format&fit=crop&q=60",
        "stock": 30
    }
]

# 執行新增動作
with app.app_context():
    # 因為你剛剛已經重建過資料庫，現在直接執行會自動把缺少的 10 項補進去
    # 既有的 10 項會因為名稱重複而被跳過 (不會重複新增)
    
    count = 0
    for item in menu_data:
        existing = MenuItem.query.filter_by(name=item['name']).first()
        if not existing:
            new_item = MenuItem(**item)
            db.session.add(new_item)
            print(f"➕ 新增餐點: {item['name']}")
            count += 1
        else:
            print(f"🔹 已存在，跳過: {item['name']}")

    db.session.commit()
    print(f"\n🎉 菜單更新完成！共新增了 {count} 項餐點。")