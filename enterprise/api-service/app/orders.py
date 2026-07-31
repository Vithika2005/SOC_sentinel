from flask import request, jsonify
from app.database import db
from app.models import Order
from app.auth import token_required

@token_required
def create_order(current_user):
    order_data = request.get_json()
    new_order = Order(product=order_data['product'], quantity=order_data['quantity'], user_id=current_user.id)
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Order created successfully'}), 201