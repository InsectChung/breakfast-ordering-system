from flask import Blueprint, request, jsonify
from models import db, Order, OrderItem, MenuItem

orders_bp = Blueprint('orders_bp', __name__)

@orders_bp.route('/orders', methods=['POST'])
def create_order():
    """
    建立新訂單
    POST /api/v1/orders
    Body: {
        "user_id": "uuid",
        "items": [{"menu_item_id": "uuid", "quantity": 1}, ...],
        "payment_method": "cash"
    }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400

    user_id = data.get('user_id')
    items = data.get('items')
    payment_method = data.get('payment_method', 'cash')

    if not user_id or not items:
        return jsonify({'error': 'Missing user_id or items'}), 400

    try:
        # 初始化訂單物件 (total_amount 稍後計算)
        new_order = Order(
            user_id=user_id,
            payment_method=payment_method,
            status='pending',
            total_amount=0
        )

        total_amount = 0.0
        
        for item_data in items:
            menu_item_id = item_data.get('menu_item_id')
            quantity = item_data.get('quantity')

            if not menu_item_id or not isinstance(quantity, int) or quantity <= 0:
                continue

            # 查詢菜單項目並檢查庫存
            menu_item = MenuItem.query.get(menu_item_id)
            if not menu_item:
                return jsonify({'error': f'Menu item {menu_item_id} not found'}), 404
            
            if menu_item.stock < quantity:
                return jsonify({'error': f'Insufficient stock for {menu_item.name}'}), 400

            # 扣除庫存
            menu_item.stock -= quantity

            # 計算金額
            item_total = menu_item.price * quantity
            total_amount += item_total

            # 建立訂單項目並加入關聯
            order_item = OrderItem(
                menu_item_id=menu_item_id,
                quantity=quantity,
                unit_price=menu_item.price
            )
            new_order.items.append(order_item)

        new_order.total_amount = total_amount

        db.session.add(new_order)
        db.session.commit()

        return jsonify({
            'message': 'Order created successfully',
            'order_id': new_order.order_id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500