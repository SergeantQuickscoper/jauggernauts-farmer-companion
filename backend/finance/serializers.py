from rest_framework import serializers
from .models import (
    FinanceAccount, Transaction, ExpenseCategory, IncomeCategory,
    Budget, CropFinance, FinancialGoal
)


class FinanceAccountSerializer(serializers.ModelSerializer):
    """Serializer for FinanceAccount model"""

    class Meta:
        model = FinanceAccount
        fields = [
            'id', 'account_name', 'account_type', 'account_number', 
            'bank_name', 'current_balance', 'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ExpenseCategorySerializer(serializers.ModelSerializer):
    """Serializer for ExpenseCategory model"""

    class Meta:
        model = ExpenseCategory
        fields = ['id', 'name', 'description', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class IncomeCategorySerializer(serializers.ModelSerializer):
    """Serializer for IncomeCategory model"""

    class Meta:
        model = IncomeCategory
        fields = ['id', 'name', 'description', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for Transaction model (read operations)"""
    account_name = serializers.CharField(source='account.account_name', read_only=True)
    to_account_name = serializers.CharField(source='to_account.account_name', read_only=True)
    expense_category_name = serializers.CharField(source='expense_category.name', read_only=True)
    income_category_name = serializers.CharField(source='income_category.name', read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id', 'account', 'account_name', 'transaction_type', 'amount', 
            'description', 'expense_category', 'expense_category_name',
            'income_category', 'income_category_name', 'to_account', 
            'to_account_name', 'transaction_date', 'created_at', 'updated_at',
            'reference_number', 'notes', 'receipt_image'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class TransactionCreateSerializer(serializers.ModelSerializer):
    """Serializer for Transaction model (create/update operations)"""

    class Meta:
        model = Transaction
        fields = [
            'account', 'transaction_type', 'amount', 'description',
            'expense_category', 'income_category', 'to_account',
            'transaction_date', 'reference_number', 'notes', 'receipt_image'
        ]

    def validate(self, data):
        """Validate transaction data"""
        transaction_type = data.get('transaction_type')

        if transaction_type == 'EXPENSE' and not data.get('expense_category'):
            raise serializers.ValidationError(
                "Expense category is required for expense transactions"
            )

        if transaction_type == 'INCOME' and not data.get('income_category'):
            raise serializers.ValidationError(
                "Income category is required for income transactions"
            )

        if transaction_type == 'TRANSFER' and not data.get('to_account'):
            raise serializers.ValidationError(
                "To account is required for transfer transactions"
            )

        if transaction_type == 'TRANSFER' and data.get('account') == data.get('to_account'):
            raise serializers.ValidationError(
                "Source and destination accounts cannot be the same"
            )

        # Validate amount is positive
        amount = data.get('amount')
        if amount and amount <= 0:
            raise serializers.ValidationError("Amount must be positive")

        return data

    def validate_account(self, value):
        """Validate that account belongs to the current user"""
        if value.farmer != self.context['request'].user:
            raise serializers.ValidationError("Invalid account")
        return value

    def validate_to_account(self, value):
        """Validate that to_account belongs to the current user"""
        if value and value.farmer != self.context['request'].user:
            raise serializers.ValidationError("Invalid destination account")
        return value


class BudgetSerializer(serializers.ModelSerializer):
    """Serializer for Budget model (read operations)"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    remaining_amount = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    percentage_used = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)

    class Meta:
        model = Budget
        fields = [
            'id', 'name', 'category', 'category_name', 'budgeted_amount',
            'spent_amount', 'remaining_amount', 'percentage_used',
            'start_date', 'end_date', 'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'spent_amount', 'created_at', 'updated_at']


class BudgetCreateSerializer(serializers.ModelSerializer):
    """Serializer for Budget model (create/update operations)"""

    class Meta:
        model = Budget
        fields = [
            'name', 'category', 'budgeted_amount', 'start_date', 'end_date', 'is_active'
        ]

    def validate(self, data):
        """Validate budget data"""
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date and end_date and start_date >= end_date:
            raise serializers.ValidationError(
                "End date must be after start date"
            )

        budgeted_amount = data.get('budgeted_amount')
        if budgeted_amount and budgeted_amount <= 0:
            raise serializers.ValidationError("Budget amount must be positive")

        return data


class CropFinanceSerializer(serializers.ModelSerializer):
    """Serializer for CropFinance model"""
    total_investment = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    profit_loss = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    roi_percentage = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)

    class Meta:
        model = CropFinance
        fields = [
            'id', 'crop_name', 'season', 'year', 'seed_cost', 'fertilizer_cost',
            'pesticide_cost', 'labor_cost', 'irrigation_cost', 'equipment_cost',
            'other_costs', 'total_investment', 'total_revenue', 'profit_loss',
            'roi_percentage', 'area_acres', 'expected_yield', 'actual_yield',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        """Validate crop finance data"""
        area_acres = data.get('area_acres')
        if area_acres and area_acres <= 0:
            raise serializers.ValidationError("Area must be positive")

        year = data.get('year')
        if year and (year < 1900 or year > 2100):
            raise serializers.ValidationError("Invalid year")

        # Validate that all cost fields are non-negative
        cost_fields = [
            'seed_cost', 'fertilizer_cost', 'pesticide_cost', 'labor_cost',
            'irrigation_cost', 'equipment_cost', 'other_costs', 'total_revenue'
        ]

        for field in cost_fields:
            value = data.get(field)
            if value and value < 0:
                raise serializers.ValidationError(f"{field} cannot be negative")

        return data


class FinancialGoalSerializer(serializers.ModelSerializer):
    """Serializer for FinancialGoal model"""
    remaining_amount = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    percentage_achieved = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    goal_type_display = serializers.CharField(source='get_goal_type_display', read_only=True)

    class Meta:
        model = FinancialGoal
        fields = [
            'id', 'goal_name', 'goal_type', 'goal_type_display', 'target_amount',
            'current_amount', 'remaining_amount', 'percentage_achieved', 
            'target_date', 'description', 'created_at', 'updated_at', 'is_achieved'
        ]
        read_only_fields = ['id', 'current_amount', 'created_at', 'updated_at', 'is_achieved']

    def validate(self, data):
        """Validate financial goal data"""
        target_amount = data.get('target_amount')
        if target_amount and target_amount <= 0:
            raise serializers.ValidationError("Target amount must be positive")

        target_date = data.get('target_date')
        if target_date and target_date < timezone.now().date():
            raise serializers.ValidationError("Target date cannot be in the past")

        return data


# Additional serializers for dashboard and analytics

class DashboardSummarySerializer(serializers.Serializer):
    """Serializer for dashboard summary data"""
    total_balance = serializers.DecimalField(max_digits=15, decimal_places=2)
    monthly_income = serializers.DecimalField(max_digits=15, decimal_places=2)
    monthly_expense = serializers.DecimalField(max_digits=15, decimal_places=2)
    net_cash_flow = serializers.DecimalField(max_digits=15, decimal_places=2)
    active_budgets_count = serializers.IntegerField()
    overbudget_count = serializers.IntegerField()
    active_goals_count = serializers.IntegerField()
    achieved_goals_count = serializers.IntegerField()


class MonthlyTrendSerializer(serializers.Serializer):
    """Serializer for monthly trend data"""
    month = serializers.CharField()
    income = serializers.DecimalField(max_digits=15, decimal_places=2)
    expense = serializers.DecimalField(max_digits=15, decimal_places=2)
    net_flow = serializers.DecimalField(max_digits=15, decimal_places=2)


class CategorySpendingSerializer(serializers.Serializer):
    """Serializer for category-wise spending data"""
    category_name = serializers.CharField()
    amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    percentage = serializers.DecimalField(max_digits=5, decimal_places=2)
    transaction_count = serializers.IntegerField()
