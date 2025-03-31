from flask import Flask
from config import db
from datetime import datetime

class WholesaleSales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gas_type = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    cylinders_sold = db.Column(db.Integer, nullable=False)
    buyer_name = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="Pending")  # Paid / Pending
    date_sold = db.Column(db.DateTime, default=datetime.utcnow)

class RetailSales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gas_type = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    cylinders_sold = db.Column(db.Integer, nullable=False)
    buyer_name = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="Pending")  # Paid / Pending
    date_sold = db.Column(db.DateTime, default=datetime.utcnow)

class GasStock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gas_type = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date_received = db.Column(db.DateTime, default=datetime.utcnow)


class PulledMoney(db.Model):
    __tablename__ = "pulledmoney"
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total_money = db.Column(db.Float, nullable=False)
    pulled_money = db.Column(db.Float, nullable=False)
    total_left = db.Column(db.Float, nullable=False)

    def __init__(self, total_money, pulled_money, total_left):
        self.total_money = total_money
        self.pulled_money = pulled_money
        self.total_left = total_left

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'total_money': self.total_money,
            'pulled_money': self.pulled_money,
            'total_left': self.total_left
        }
