from flask import Blueprint, request, jsonify
from models import PulledMoney
from config import db

pulled_money_bp = Blueprint('pulled_money', __name__)

@pulled_money_bp.route('/pulled-money', methods=['POST'])
def create_pulled_money():
    data = request.get_json()
    
    try:
        # Calculate total left
        total_left = float(data['total_money']) - float(data['pulled_money'])
        
        new_entry = PulledMoney(
            total_money=data['total_money'],
            pulled_money=data['pulled_money'],
            total_left=total_left
        )
        
        db.session.add(new_entry)
        db.session.commit()
        
        return jsonify({
            'message': 'Pulled money record created successfully',
            'data': new_entry.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@pulled_money_bp.route('/pulled-money', methods=['GET'])
def get_all_pulled_money():
    try:
        records = PulledMoney.query.order_by(PulledMoney.date.desc()).all()
        return jsonify([record.to_dict() for record in records]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@pulled_money_bp.route('/pulled-money/<int:id>', methods=['GET'])
def get_pulled_money(id):
    try:
        record = PulledMoney.query.get_or_404(id)
        return jsonify(record.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@pulled_money_bp.route('/pulled-money/<int:id>', methods=['PUT'])
def update_pulled_money(id):
    data = request.get_json()
    
    try:
        record = PulledMoney.query.get_or_404(id)
        
        # Update fields if they exist in the request
        if 'total_money' in data:
            record.total_money = float(data['total_money'])
        if 'pulled_money' in data:
            record.pulled_money = float(data['pulled_money'])
        
        # Recalculate total left if any money values changed
        if 'total_money' in data or 'pulled_money' in data:
            record.total_left = record.total_money - record.pulled_money
        
        db.session.commit()
        
        return jsonify({
            'message': 'Pulled money record updated successfully',
            'data': record.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@pulled_money_bp.route('/pulled-money/<int:id>', methods=['DELETE'])
def delete_pulled_money(id):
    try:
        record = PulledMoney.query.get_or_404(id)
        db.session.delete(record)
        db.session.commit()
        return jsonify({'message': 'Pulled money record deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400