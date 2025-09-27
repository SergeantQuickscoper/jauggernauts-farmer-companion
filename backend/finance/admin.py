from django.contrib import admin
from .models import (
    FinanceAccount, Transaction, ExpenseCategory, IncomeCategory,
    Budget, CropFinance, FinancialGoal
)


@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(IncomeCategory)
class IncomeCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(FinanceAccount)
class FinanceAccountAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'account_name', 'account_type', 'current_balance', 'is_active', 'created_at']
    list_filter = ['account_type', 'is_active', 'created_at']
    search_fields = ['farmer__username', 'account_name', 'account_number', 'bank_name']
    ordering = ['-created_at']
    readonly_fields = ['current_balance', 'created_at', 'updated_at']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'transaction_type', 'amount', 'account', 'transaction_date', 'created_at']
    list_filter = ['transaction_type', 'transaction_date', 'created_at', 'expense_category', 'income_category']
    search_fields = ['farmer__username', 'description', 'reference_number']
    ordering = ['-transaction_date']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'transaction_date'

    fieldsets = (
        ('Basic Information', {
            'fields': ('farmer', 'account', 'transaction_type', 'amount', 'description')
        }),
        ('Category Information', {
            'fields': ('expense_category', 'income_category', 'to_account')
        }),
        ('Date Information', {
            'fields': ('transaction_date', 'created_at', 'updated_at')
        }),
        ('Additional Information', {
            'fields': ('reference_number', 'notes', 'receipt_image'),
            'classes': ['collapse']
        }),
    )


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'name', 'category', 'budgeted_amount', 'spent_amount', 'remaining_amount', 'start_date', 'end_date']
    list_filter = ['category', 'start_date', 'end_date', 'is_active']
    search_fields = ['farmer__username', 'name']
    ordering = ['-created_at']
    readonly_fields = ['spent_amount', 'created_at', 'updated_at']

    def remaining_amount(self, obj):
        return obj.remaining_amount
    remaining_amount.short_description = 'Remaining Amount'


@admin.register(CropFinance)
class CropFinanceAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'crop_name', 'season', 'year', 'area_acres', 'total_investment', 'total_revenue', 'profit_loss']
    list_filter = ['season', 'year', 'crop_name']
    search_fields = ['farmer__username', 'crop_name']
    ordering = ['-year', '-created_at']
    readonly_fields = ['total_investment', 'profit_loss', 'roi_percentage', 'created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('farmer', 'crop_name', 'season', 'year', 'area_acres')
        }),
        ('Costs', {
            'fields': ('seed_cost', 'fertilizer_cost', 'pesticide_cost', 'labor_cost', 'irrigation_cost', 'equipment_cost', 'other_costs')
        }),
        ('Revenue & Yield', {
            'fields': ('total_revenue', 'expected_yield', 'actual_yield')
        }),
        ('Calculated Fields', {
            'fields': ('total_investment', 'profit_loss', 'roi_percentage'),
            'classes': ['collapse']
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ['collapse']
        }),
    )

    def total_investment(self, obj):
        return obj.total_investment
    total_investment.short_description = 'Total Investment'

    def profit_loss(self, obj):
        return obj.profit_loss
    profit_loss.short_description = 'Profit/Loss'


@admin.register(FinancialGoal)
class FinancialGoalAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'goal_name', 'goal_type', 'target_amount', 'current_amount', 'percentage_achieved', 'target_date', 'is_achieved']
    list_filter = ['goal_type', 'is_achieved', 'target_date']
    search_fields = ['farmer__username', 'goal_name']
    ordering = ['-created_at']
    readonly_fields = ['percentage_achieved', 'remaining_amount', 'created_at', 'updated_at']

    def percentage_achieved(self, obj):
        return f"{obj.percentage_achieved:.2f}%"
    percentage_achieved.short_description = 'Progress'

    def remaining_amount(self, obj):
        return obj.remaining_amount
    remaining_amount.short_description = 'Remaining'
