from flask import Blueprint, request, jsonify
from config import db
from models import GasStock

stock_bp = Blueprint('stock', __name__)

# Create
@stock_bp.route('/stock/add', methods=['POST'])
def add_stock():
    data = request.json
    new_stock = GasStock(
        gas_type=data['gas_type'],
        quantity=data['quantity']
    )
    db.session.add(new_stock)
    db.session.commit()
    return jsonify({"message": "Stock record added successfully"}), 201

# Read All
@stock_bp.route('/stock/all', methods=['GET'])
def get_stock():
    stock = GasStock.query.order_by(GasStock.date_received.desc()).all()
    return jsonify([{
        "id": s.id,
        "gas_type": s.gas_type,
        "quantity": s.quantity,
        "date_received": s.date_received
    } for s in stock])

# Read Single
@stock_bp.route('/stock/<int:stock_id>', methods=['GET'])
def get_single_stock(stock_id):
    stock = GasStock.query.get(stock_id)
    if not stock:
        return jsonify({"message": "Stock record not found"}), 404
    return jsonify({
        "id": stock.id,
        "gas_type": stock.gas_type,
        "quantity": stock.quantity,
        "date_received": stock.date_received
    })

# Update
@stock_bp.route('/stock/update/<int:stock_id>', methods=['PUT'])
def update_stock(stock_id):
    stock = GasStock.query.get(stock_id)
    if not stock:
        return jsonify({"message": "Stock record not found"}), 404
    
    data = request.json
    stock.gas_type = data.get('gas_type', stock.gas_type)
    stock.quantity = data.get('quantity', stock.quantity)
    
    db.session.commit()
    return jsonify({"message": "Stock record updated successfully"}), 200

# Delete
@stock_bp.route('/stock/delete/<int:stock_id>', methods=['DELETE'])
def delete_stock(stock_id):
    stock = GasStock.query.get(stock_id)
    if not stock:
        return jsonify({"message": "Stock record not found"}), 404
    
    db.session.delete(stock)
    db.session.commit()
    return jsonify({"message": "Stock record deleted successfully"}), 200