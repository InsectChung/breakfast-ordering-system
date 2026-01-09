from flask import Blueprint, request, jsonify
from models import MenuItem

menu_bp = Blueprint('menu_bp', __name__)

@menu_bp.route('/menu', methods=['GET'])
def get_menu():
    """
    取得菜單列表
    GET /api/v1/menu
    支援參數: category (選填)
    """
    category = request.args.get('category')
    
    query = MenuItem.query
    
    if category:
        query = query.filter_by(category=category)
        
    menu_items = query.all()
    
    return jsonify([item.to_dict() for item in menu_items]), 200
