from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json
from .models import Account, Transaction

def get_account_balance(request):
    user = request.user
    account = get_object_or_404(Account, user=user)
    return JsonResponse({'balance': str(account.balance)}, status=200)

def list_transactions(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user).order_by('-timestamp')
    transactions_data = [
        {
            'name' : tx.name,
            'amount': str(abs(tx.amount)),
            'timestamp': tx.timestamp.isoformat(),
            'description': tx.description,
            'category': tx.category,
            'id': tx.id,
            'type': 'revenue' if tx.amount > 0 else 'expense'
        } for tx in transactions
    ]
    return JsonResponse({'transactions': transactions_data}, status=200)

def create_transaction(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        amount = data.get('amount')
        description = data.get('description', '')
        category = data.get('category', '')
        name = data.get('name', '')
        if amount is None:
            return JsonResponse({'error': 'Amount is required'}, status=400)

        user = request.user
        account = get_object_or_404(Account, user=user)

        account.balance += Decimal(amount)
        account.save()

        transaction = Transaction.objects.create(
            name=name,
            category=category,
            user=user,
            amount=Decimal(amount),
            description=description,
        )

        return JsonResponse({
            'message': 'Transaction created successfully',
            'transaction': {
                'amount': str(transaction.amount),
                'timestamp': transaction.timestamp.isoformat(),
                'description': transaction.description,
                'id': transaction.id,
            },
            'new_balance': str(account.balance)
        }, status=201)

    return JsonResponse({'error': 'Only POST allowed'}, status=405)

def delete_transaction(request, transaction_id):
    if request.method == 'DELETE':
        user = request.user
        transaction = get_object_or_404(Transaction, id=transaction_id, user=user)
        account = get_object_or_404(Account, user=user)

        account.balance -= transaction.amount
        account.save()

        transaction.delete()

        return JsonResponse({'message': 'Transaction deleted successfully', 'new_balance': str(account.balance)}, status=200)

    return JsonResponse({'error': 'Only DELETE allowed'}, status=405)