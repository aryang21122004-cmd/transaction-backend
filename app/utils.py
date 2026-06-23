def validate_transaction(data):
    errors = []

    if not data.get('userId'):
        errors.append('userId is required to identify the user')
    elif len(data['userId'].strip()) == 0:
        errors.append('userId cannot be blank spaces')

    if not data.get('transactionId'):
        errors.append('transactionId is required - each transaction needs a unique ID')

    if 'amount' not in data:
        errors.append('amount is missing')
    elif not isinstance(data['amount'], (int, float)):
        errors.append('amount should be a number')
    elif data['amount'] <= 0:
        errors.append('amount must be greater than 0 - negative or zero transactions not allowed')

    return errors