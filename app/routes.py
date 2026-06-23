from flask import Blueprint, request, jsonify
from app.utils import validate_transaction
from app.services import process_transaction, get_user_summary, get_ranking


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