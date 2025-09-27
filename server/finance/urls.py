from django.urls import path, include
from . import views


urlpatterns = [
    path('get_account_balance/', views.get_account_balance, name='get_account_balance'),
    path('list_transactions/', views.list_transactions, name='list_transactions'),
    path('create_transaction/', views.create_transaction, name='create_transaction'),
    path('delete_transaction/<int:transaction_id>/', views.delete_transaction, name='delete_transaction'),
]