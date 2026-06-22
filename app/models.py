from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(100), primary_key=True)
    total_amount = db.Column(db.Float, default=0.0)
    transaction_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_transaction_at = db.Column(db.DateTime, nullable=True)

    transactions = db.relationship('Transaction', backref='user', lazy=True)

    def to_dict(self):
        return {
            'userId': self.id,
            'totalAmount': self.total_amount,
            'transactionCount': self.transaction_count,
        }


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.String(100), primary_key=True)
    user_id = db.Column(db.String(100), db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'transactionId': self.id,
            'userId': self.user_id,
            'amount': self.amount,
        }