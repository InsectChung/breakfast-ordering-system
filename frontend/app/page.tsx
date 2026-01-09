"use client";

import { useState, useEffect } from "react";
import axios from "axios";

// 定義資料結構
interface MenuItem {
  id: string;
  name: string;
  description: string;
  price: number;
  image_url: string;
  stock: number;
}

interface CartItem {
  menuItemId: string;
  name: string;
  price: number;
  quantity: number;
}

export default function Home() {
  const [menu, setMenu] = useState<MenuItem[]>([]);
  const [cart, setCart] = useState<CartItem[]>([]);
  const [userId, setUserId] = useState("");
  const [loading, setLoading] = useState(true);

  // 1. 載入菜單
  useEffect(() => {
    const fetchMenu = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/v1/menu");
        setMenu(response.data);
      } catch (error) {
        console.error("無法取得菜單:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchMenu();
  }, []);

  // 2. 加入購物車邏輯
  const addToCart = (item: MenuItem) => {
    setCart((prev) => {
      const existing = prev.find((i) => i.menuItemId === item.id);
      if (existing) {
        return prev.map((i) =>
          i.menuItemId === item.id ? { ...i, quantity: i.quantity + 1 } : i
        );
      }
      return [
        ...prev,
        { menuItemId: item.id, name: item.name, price: item.price, quantity: 1 },
      ];
    });
  };

  // 🔥 新增功能：調整購物車數量 (減少到0會自動移除)
  const updateCartQuantity = (itemId: string, delta: number) => {
    setCart((prev) => {
      return prev.map((item) => {
          if (item.menuItemId === itemId) {
            return { ...item, quantity: item.quantity + delta };
          }
          return item;
        })
        .filter((item) => item.quantity > 0); // 過濾掉數量 <= 0 的商品
    });
  };

  // 🔥 新增功能：直接移除某項商品
  const removeFromCart = (itemId: string) => {
    setCart((prev) => prev.filter((item) => item.menuItemId !== itemId));
  };

  // 3. 送出訂單邏輯
  const handleCheckout = async () => {
    if (!userId) {
      alert("請先輸入 User ID (可從 create_user.py 取得)");
      return;
    }
    if (cart.length === 0) {
      alert("購物車是空的！");
      return;
    }

    const payload = {
      user_id: userId,
      payment_method: "cash",
      items: cart.map((item) => ({
        menu_item_id: item.menuItemId,
        quantity: item.quantity,
      })),
    };

    try {
      const response = await axios.post("http://127.0.0.1:5000/api/v1/orders", payload);
      alert(`🎉 訂單成功！Order ID: ${response.data.order_id}`);
      setCart([]);
    } catch (error) {
      console.error("下單失敗:", error);
      let errorMessage = "發生未知錯誤";
      if (axios.isAxiosError(error) && error.response) {
        errorMessage = error.response.data.error || error.message;
      } else if (error instanceof Error) {
        errorMessage = error.message;
      }
      alert(`❌ 下單失敗: ${errorMessage}`);
    }
  };

  // 計算總金額
  const totalPrice = cart.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  );

  if (loading) return <div className="p-10 text-center">載入菜單中...</div>;

  return (
    // 🔥 修改背景顏色：將 bg-gray-50 改為 bg-orange-50 (溫暖色系)
    <main className="min-h-screen p-8 bg-orange-50 flex flex-col md:flex-row gap-8">
      
      {/* 左側：菜單區 */}
      <div className="flex-1">
        <h1 className="text-4xl font-extrabold mb-6 text-orange-800 drop-shadow-sm">
          🌞 快樂早餐店
        </h1>

        {/* User ID 輸入區 */}
        <div className="mb-6 bg-white p-4 rounded-xl shadow-sm border border-orange-100">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            請輸入您的 User ID (測試用):
          </label>
          <input
            type="text"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            placeholder="例如: 4a94206e-..."
            className="w-full p-2 border border-gray-300 rounded focus:ring-2 focus:ring-orange-300 outline-none"
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {menu.map((item) => (
            <div
              key={item.id}
              className="bg-white rounded-xl shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden group"
            >
              <div className="h-48 bg-gray-200 relative overflow-hidden">
                <img
                  src={item.image_url}
                  alt={item.name}
                  className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                />
              </div>
              <div className="p-5">
                <div className="flex justify-between items-center mb-2">
                  <h3 className="font-bold text-xl text-gray-800">{item.name}</h3>
                  <span className="text-orange-600 font-bold text-lg">
                    ${item.price}
                  </span>
                </div>
                <p className="text-gray-500 text-sm mb-4 line-clamp-2">
                  {item.description}
                </p>
                <button
                  onClick={() => addToCart(item)}
                  disabled={item.stock <= 0}
                  className="w-full bg-orange-500 text-white py-2 rounded-lg font-medium hover:bg-orange-600 active:scale-95 transition disabled:bg-gray-300"
                >
                  {item.stock > 0 ? "加入購物車 🛒" : "已售完 ❌"}
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 右側：購物車區 */}
      <div className="w-full md:w-96 h-fit sticky top-8">
        <div className="bg-white p-6 rounded-xl shadow-lg border border-orange-100">
          <h2 className="text-2xl font-bold mb-4 border-b pb-3 text-gray-800 flex items-center gap-2">
            🛒 您的購物車
          </h2>

          {cart.length === 0 ? (
            <div className="text-center py-10 text-gray-400 bg-gray-50 rounded-lg border border-dashed border-gray-300">
              <p>購物車是空的</p>
              <p className="text-sm mt-1">快去選點好吃的吧！</p>
            </div>
          ) : (
            <ul className="space-y-4 mb-6 max-h-[60vh] overflow-y-auto pr-2 custom-scrollbar">
              {cart.map((item) => (
                <li
                  key={item.menuItemId}
                  className="flex flex-col border-b border-gray-100 pb-3 last:border-0"
                >
                  <div className="flex justify-between items-start mb-2">
                    <span className="font-medium text-gray-800">{item.name}</span>
                    <span className="font-bold text-gray-900">
                      ${item.price * item.quantity}
                    </span>
                  </div>
                  
                  {/* 🔥 新增功能：數量控制按鈕 */}
                  <div className="flex justify-between items-center">
                    <div className="flex items-center gap-3 bg-gray-100 rounded-lg p-1">
                      <button
                        onClick={() => updateCartQuantity(item.menuItemId, -1)}
                        className="w-8 h-8 flex items-center justify-center bg-white rounded shadow-sm hover:bg-red-50 text-red-500 font-bold transition"
                      >
                        -
                      </button>
                      <span className="font-bold w-4 text-center text-sm">
                        {item.quantity}
                      </span>
                      <button
                        onClick={() => updateCartQuantity(item.menuItemId, 1)}
                        className="w-8 h-8 flex items-center justify-center bg-white rounded shadow-sm hover:bg-green-50 text-green-600 font-bold transition"
                      >
                        +
                      </button>
                    </div>
                    
                    <button 
                        onClick={() => removeFromCart(item.menuItemId)}
                        className="text-xs text-gray-400 hover:text-red-500 underline decoration-dotted"
                    >
                        移除
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          )}

          <div className="border-t pt-4 mt-4">
            <div className="flex justify-between text-xl font-bold mb-6 text-gray-800">
              <span>總計金額:</span>
              <span className="text-orange-600">${totalPrice}</span>
            </div>
            <button
              onClick={handleCheckout}
              disabled={cart.length === 0}
              className="w-full bg-green-500 text-white py-3 rounded-xl font-bold text-lg hover:bg-green-600 disabled:bg-gray-300 shadow-md hover:shadow-lg transition transform active:scale-98"
            >
              確認結帳 ✨
            </button>
          </div>
        </div>
      </div>
    </main>
  );
}