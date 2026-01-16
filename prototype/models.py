from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)
    full_name = db.Column(db.String(100))
    department = db.Column(db.String(100))

class ToolHolder(db.Model):
    __tablename__ = 'tool_holders'
    id = db.Column(db.Integer, primary_key=True)
    iso_code = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50))
    description = db.Column(db.String(200))
    location = db.Column(db.String(50))
    stock = db.Column(db.Integer, default=0)
    # Simple JSON storage for compatible inserts list in this MVP
    compatible_inserts_json = db.Column(db.String(500), default="[]")

class Insert(db.Model):
    __tablename__ = 'inserts'
    id = db.Column(db.Integer, primary_key=True)
    iso_code = db.Column(db.String(50), nullable=False)
    grade = db.Column(db.String(50))
    material_app = db.Column(db.String(50)) # e.g. Steel (P)
    coating = db.Column(db.String(50))
    manufacturer = db.Column(db.String(50))
    stock_quantity = db.Column(db.Integer, default=0)
    min_alert_level = db.Column(db.Integer, default=10)
    box_quantity = db.Column(db.Integer, default=10)

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    item_type = db.Column(db.String(20)) # 'tool' or 'insert'
    item_id = db.Column(db.Integer)
    transaction_type = db.Column(db.String(20)) # 'checkout', 'return'
    quantity = db.Column(db.Integer, default=1)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
