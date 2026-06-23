from flask import Blueprint, request, jsonify
from app.utils import validate_transaction
from app.services import process_transaction, get_user_summary, get_ranking
from app.models import User, Transaction
from app import db
main = Blueprint('main', __name__)

@main.route('/transaction', methods=['POST'])
def create_transaction():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400

    errors = validate_transaction(data)
    if errors:
        return jsonify({'errors': errors}), 400

    result, status = process_transaction(
        user_id=data['userId'],
        amount=data['amount'],
        transaction_id=data['transactionId']
    )
    return jsonify(result), status


@main.route('/summary/<user_id>', methods=['GET'])
def user_summary(user_id):
    result, status = get_user_summary(user_id)
    return jsonify(result), status


@main.route('/ranking', methods=['GET'])
def ranking():
    result, status = get_ranking()
    return jsonify(result), status

@main.route('/reset', methods=['DELETE'])
def reset():
    db.session.query(Transaction).delete()
    db.session.query(User).delete()
    db.session.commit()
    return jsonify({'message': 'Database cleared'}), 200
