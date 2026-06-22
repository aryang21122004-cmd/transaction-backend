def validate_transaction(data):
    errors = []

    if not data.get('userId'):
        errors.append('userId is required')

    if not data.get('transactionId'):
        errors.append('transactionId is required')

    if 'amount' not in data:
        errors.append('amount is required')
    elif not isinstance(data['amount'], (int, float)):
        errors.append('amount must be a number')
    elif data['amount'] <= 0:
        errors.append('amount must be greater than 0')

    return errors