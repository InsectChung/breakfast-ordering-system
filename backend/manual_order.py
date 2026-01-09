import requests
import json

# 設定 API 網址
url = "http://127.0.0.1:5000/api/v1/orders"

# 準備訂單資料
payload = {
    "user_id": "4a94206e-46ad-4e61-ada8-d2a3a29a0d96",  # 您的 User ID
    "payment_method": "cash",
    "items": [
        {
            # 這是「經典蛋餅」的 ID (來自您之前的截圖)
            "menu_item_id": "3f196ed3-b69b-416f-93c3-8a5e39a4b599", 
            "quantity": 2
        }
    ]
}

# 設定標頭
headers = {
    "Content-Type": "application/json"
}

print(f"正在發送訂單給 {url} ...")
print(f"訂單內容: {json.dumps(payload, indent=2, ensure_ascii=False)}")

try:
    # 發送 POST 請求
    response = requests.post(url, json=payload, headers=headers)
    
    # 顯示結果
    print("\n--- 伺服器回應 ---")
    print(f"狀態碼: {response.status_code}")
    print(response.json())
    
    if response.status_code == 201:
        print("\n✅ 測試成功！訂單已建立！")
    else:
        print("\n❌ 測試失敗，請檢查錯誤訊息。")

except Exception as e:
    print(f"\n❌ 連線錯誤: {e}")
    print("請確認 python app.py 是否正在執行中？")