from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class FinanceAccount(models.Model):
    """Model to represent different finance accounts for a farmer"""
    ACCOUNT_TYPES = [
        ('SAVINGS', 'Savings Account'),
        ('CURRENT', 'Current Account'),
        ('LOAN', 'Loan Account'),
        ('CREDIT', 'Credit Account'),
        ('CASH', 'Cash'),
    ]

    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='finance_accounts')
    account_name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    current_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'finance_accounts'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.farmer.username} - {self.account_name}"


class ExpenseCategory(models.Model):
    """Model for expense categories"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'expense_categories'
        verbose_name_plural = 'Expense Categories'

    def __str__(self):
        return self.name


class IncomeCategory(models.Model):
    """Model for income categories"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'income_categories'
        verbose_name_plural = 'Income Categories'

    def __str__(self):
        return self.name


class Transaction(models.Model):
    """Model to track all financial transactions"""
    TRANSACTION_TYPES = [
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
        ('TRANSFER', 'Transfer'),
    ]

    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    account = models.ForeignKey(FinanceAccount, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField()

    # Categories
    expense_category = models.ForeignKey(ExpenseCategory, on_delete=models.SET_NULL, null=True, blank=True)
    income_category = models.ForeignKey(IncomeCategory, on_delete=models.SET_NULL, null=True, blank=True)

    # Transfer related fields
    to_account = models.ForeignKey(FinanceAccount, on_delete=models.SET_NULL, null=True, blank=True, related_name='incoming_transfers')

    transaction_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Additional metadata
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    receipt_image = models.ImageField(upload_to='transaction_receipts/', blank=True, null=True)

    class Meta:
        db_table = 'transactions'
        ordering = ['-transaction_date']

    def __str__(self):
        return f"{self.farmer.username} - {self.transaction_type} - ₹{self.amount}"

    def save(self, *args, **kwargs):
        """Override save to update account balance"""
        is_new = self._state.adding
        old_transaction = None

        if not is_new:
            old_transaction = Transaction.objects.get(pk=self.pk)

        super().save(*args, **kwargs)

        # Update account balance
        self.update_account_balance(old_transaction)

    def delete(self, *args, **kwargs):
        """Override delete to update account balance"""
        account = self.account
        to_account = self.to_account

        super().delete(*args, **kwargs)

        # Reverse the transaction impact on balance
        if self.transaction_type == 'INCOME':
            account.current_balance -= self.amount
        elif self.transaction_type == 'EXPENSE':
            account.current_balance += self.amount
        elif self.transaction_type == 'TRANSFER':
            account.current_balance += self.amount
            if to_account:
                to_account.current_balance -= self.amount
                to_account.save()

        account.save()

    def update_account_balance(self, old_transaction=None):
        """Update account balances based on transaction"""
        account = self.account
        to_account = self.to_account

        # If updating existing transaction, reverse old impact first
        if old_transaction:
            if old_transaction.transaction_type == 'INCOME':
                account.current_balance -= old_transaction.amount
            elif old_transaction.transaction_type == 'EXPENSE':
                account.current_balance += old_transaction.amount
            elif old_transaction.transaction_type == 'TRANSFER':
                account.current_balance += old_transaction.amount
                if old_transaction.to_account:
                    old_transaction.to_account.current_balance -= old_transaction.amount
                    old_transaction.to_account.save()

        # Apply new transaction impact
        if self.transaction_type == 'INCOME':
            account.current_balance += self.amount
        elif self.transaction_type == 'EXPENSE':
            account.current_balance -= self.amount
        elif self.transaction_type == 'TRANSFER':
            account.current_balance -= self.amount
            if to_account:
                to_account.current_balance += self.amount
                to_account.save()

        account.save()


class Budget(models.Model):
    """Model for budget planning"""
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    name = models.CharField(max_length=100)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    budgeted_amount = models.DecimalField(max_digits=15, decimal_places=2)
    spent_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    # Budget period
    start_date = models.DateField()
    end_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'budgets'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.farmer.username} - {self.name}"

    @property
    def remaining_amount(self):
        return self.budgeted_amount - self.spent_amount

    @property
    def percentage_used(self):
        if self.budgeted_amount == 0:
            return 0
        return (self.spent_amount / self.budgeted_amount) * 100


class CropFinance(models.Model):
    """Model to track finances per crop/season"""
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='crop_finances')
    crop_name = models.CharField(max_length=100)
    season = models.CharField(max_length=50)  # Kharif, Rabi, Summer
    year = models.IntegerField()

    # Investment tracking
    seed_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fertilizer_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    pesticide_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    labor_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    irrigation_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    equipment_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    other_costs = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Revenue tracking
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    # Area and yield
    area_acres = models.DecimalField(max_digits=8, decimal_places=2)
    expected_yield = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    actual_yield = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'crop_finances'
        unique_together = ['farmer', 'crop_name', 'season', 'year']
        ordering = ['-year', '-created_at']

    def __str__(self):
        return f"{self.farmer.username} - {self.crop_name} {self.season} {self.year}"

    @property
    def total_investment(self):
        return (self.seed_cost + self.fertilizer_cost + self.pesticide_cost + 
                self.labor_cost + self.irrigation_cost + self.equipment_cost + self.other_costs)

    @property
    def profit_loss(self):
        return self.total_revenue - self.total_investment

    @property
    def roi_percentage(self):
        if self.total_investment == 0:
            return 0
        return (self.profit_loss / self.total_investment) * 100


class FinancialGoal(models.Model):
    """Model for financial goals and savings targets"""
    GOAL_TYPES = [
        ('SAVINGS', 'Savings Goal'),
        ('EQUIPMENT', 'Equipment Purchase'),
        ('LAND', 'Land Purchase'),
        ('EDUCATION', 'Education'),
        ('EMERGENCY', 'Emergency Fund'),
        ('OTHER', 'Other'),
    ]

    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='financial_goals')
    goal_name = models.CharField(max_length=100)
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPES)
    target_amount = models.DecimalField(max_digits=15, decimal_places=2)
    current_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    target_date = models.DateField()

    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_achieved = models.BooleanField(default=False)

    class Meta:
        db_table = 'financial_goals'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.farmer.username} - {self.goal_name}"

    @property
    def remaining_amount(self):
        return self.target_amount - self.current_amount

    @property
    def percentage_achieved(self):
        if self.target_amount == 0:
            return 0
        return (self.current_amount / self.target_amount) * 100
