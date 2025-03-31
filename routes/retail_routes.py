from flask import Blueprint, request, jsonify
from config import db
from models import RetailSales

retail_bp = Blueprint('retail', __name__)

# Create
@retail_bp.route('/retail/add', methods=['POST'])
def add_retail():
    data = request.json
    new_sale = RetailSales(
        gas_type=data['gas_type'],
        price=data['price'],
        total=data['total'],
        cylinders_sold=data['cylinders_sold'],
        buyer_name=data['buyer_name'],
        balance=data['balance'],
        status=data.get('status', "Pending")
    )
    db.session.add(new_sale)
    db.session.commit()
    return jsonify({"message": "Retail sale added successfully"}), 201

# Read All
@retail_bp.route('/retail/all', methods=['GET'])
def get_retail_sales():
    sales = RetailSales.query.order_by(RetailSales.date_sold.desc()).all()
    return jsonify([{
        "id": sale.id,
        "gas_type": sale.gas_type,
        "price": sale.price,
        "total": sale.total,
        "cylinders_sold": sale.cylinders_sold,
        "buyer_name": sale.buyer_name,
        "balance": sale.balance,
        "status": sale.status,
        "date_sold": sale.date_sold
    } for sale in sales])

# Read Single
@retail_bp.route('/retail/<int:sale_id>', methods=['GET'])
def get_retail_sale(sale_id):
    sale = RetailSales.query.get(sale_id)
    if not sale:
        return jsonify({"message": "Sale not found"}), 404
    return jsonify({
        "id": sale.id,
        "gas_type": sale.gas_type,
        "price": sale.price,
        "total": sale.total,
        "cylinders_sold": sale.cylinders_sold,
        "buyer_name": sale.buyer_name,
        "balance": sale.balance,
        "status": sale.status,
        "date_sold": sale.date_sold
    })

# Update
@retail_bp.route('/retail/update/<int:sale_id>', methods=['PUT'])
def update_retail_sale(sale_id):
    sale = RetailSales.query.get(sale_id)
    if not sale:
        return jsonify({"message": "Sale not found"}), 404
    
    data = request.json
    sale.gas_type = data.get('gas_type', sale.gas_type)
    sale.price = data.get('price', sale.price)
    sale.total = data.get('total', sale.total)
    sale.cylinders_sold = data.get('cylinders_sold', sale.cylinders_sold)
    sale.buyer_name = data.get('buyer_name', sale.buyer_name)
    sale.balance = data.get('balance', sale.balance)
    sale.status = data.get('status', sale.status)
    
    db.session.commit()
    return jsonify({"message": "Retail sale updated successfully"}), 200

# Delete
@retail_bp.route('/retail/delete/<int:sale_id>', methods=['DELETE'])
def delete_retail_sale(sale_id):
    sale = RetailSales.query.get(sale_id)
    if not sale:
        return jsonify({"message": "Sale not found"}), 404
    
    db.session.delete(sale)
    db.session.commit()
    return jsonify({"message": "Retail sale deleted successfully"}), 200