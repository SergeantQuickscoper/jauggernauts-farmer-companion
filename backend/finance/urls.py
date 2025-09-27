from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'accounts', views.FinanceAccountViewSet, basename='finance-accounts')
router.register(r'transactions', views.TransactionViewSet, basename='transactions')
router.register(r'expense-categories', views.ExpenseCategoryViewSet, basename='expense-categories')
router.register(r'income-categories', views.IncomeCategoryViewSet, basename='income-categories')
router.register(r'budgets', views.BudgetViewSet, basename='budgets')
router.register(r'crop-finances', views.CropFinanceViewSet, basename='crop-finances')
router.register(r'financial-goals', views.FinancialGoalViewSet, basename='financial-goals')

app_name = 'finance'

urlpatterns = [
    # API endpoints
    path('api/finance/', include(router.urls)),

    # Dashboard endpoints
    path('api/finance/dashboard/summary/', views.dashboard_summary, name='dashboard-summary'),
    path('api/finance/dashboard/trends/', views.monthly_trends, name='monthly-trends'),
    path('api/finance/dashboard/expense-breakdown/', views.expense_categories_breakdown, name='expense-breakdown'),
]
