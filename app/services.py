import threading
from datetime import datetime
from app import db
from app.models import User, Transaction

transaction_lock = threading.Lock()

def process_transaction(user_id, amount, transaction_id):

    # Step 1: Check for duplicate
    existing = Transaction.query.get(transaction_id)
    if existing:
        return {'error': 'Duplicate transaction'}, 409

    # Step 2: Acquire lock before touching the database
    with transaction_lock:

        # Step 3: Get user or create if first time
        user = User.query.get(user_id)
        if not user:
            user = User(
                id=user_id,
                total_amount=0.0,
                transaction_count=0
            )
            db.session.add(user)
            db.session.flush()

        # Step 4: Create the transaction record
        txn = Transaction(
            id=transaction_id,
            user_id=user_id,
            amount=amount,
            created_at=datetime.utcnow()
        )
        db.session.add(txn)

        # Step 5: Update user totals
        user.total_amount += amount
        user.transaction_count += 1
        user.last_transaction_at = datetime.utcnow()

        # Step 6: Save everything
        db.session.commit()

    return {'message': 'Transaction recorded', 'transactionId': transaction_id}, 201
def get_user_summary(user_id):
    user = User.query.get(user_id)
    if not user:
        return {'error': 'User not found'}, 404

    all_users = User.query.all()
    ranked = sorted(all_users, key=lambda u: calculate_score(u), reverse=True)
    rank = next((i + 1 for i, u in enumerate(ranked) if u.id == user_id), None)

    return {
        'userId': user.id,
        'totalAmount': user.total_amount,
        'transactionCount': user.transaction_count,
        'rank': rank
    }, 200


def get_ranking():
    all_users = User.query.all()
    if not all_users:
        return [], 200

    ranked = sorted(all_users, key=lambda u: calculate_score(u), reverse=True)

    result = []
    for i, user in enumerate(ranked):
        result.append({
            'rank': i + 1,
            'userId': user.id,
            'totalAmount': user.total_amount,
            'transactionCount': user.transaction_count,
            'score': round(calculate_score(user), 2)
        })

    return result, 200


def calculate_score(user):
    total_amount = user.total_amount or 0.0
    transaction_count = user.transaction_count or 0
    amount_score = total_amount * 0.6
    count_score = transaction_count * 0.3
    consistency_bonus = min(transaction_count, 10) * 1.0
    return amount_score + count_score + consistency_bonus