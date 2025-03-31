from flask import Blueprint, request, jsonify
from config import db
from models import WholesaleSales

wholesale_bp = Blueprint('wholesale', __name__)

# Create
@wholesale_bp.route('/wholesale/add', methods=['POST'])
def add_wholesale():
    data = request.json
    new_sale = WholesaleSales(
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
    return jsonify({"message": "Wholesale sale added successfully"}), 201

# Read All
@wholesale_bp.route('/wholesale/all', methods=['GET'])
def get_wholesale_sales():
    sales = WholesaleSales.query.order_by(WholesaleSales.date_sold.desc()).all()
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
@wholesale_bp.route('/wholesale/<int:sale_id>', methods=['GET'])
def get_wholesale_sale(sale_id):
    sale = WholesaleSales.query.get(sale_id)
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
@wholesale_bp.route('/wholesale/update/<int:sale_id>', methods=['PUT'])
def update_wholesale_status(sale_id):
    sale = WholesaleSales.query.get(sale_id)
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
    return jsonify({"message": "Sale updated successfully"}), 200

# Delete
@wholesale_bp.route('/wholesale/delete/<int:sale_id>', methods=['DELETE'])
def delete_wholesale_sale(sale_id):
    sale = WholesaleSales.query.get(sale_id)
    if not sale:
        return jsonify({"message": "Sale not found"}), 404
    
    db.session.delete(sale)
    db.session.commit()
    return jsonify({"message": "Sale deleted successfully"}), 200