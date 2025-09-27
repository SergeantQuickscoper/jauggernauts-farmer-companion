from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Transaction, Budget, ExpenseCategory, IncomeCategory


@receiver(post_save, sender=Transaction)
def update_budget_spent_amount(sender, instance, **kwargs):
    """Update budget spent amount when expense transaction is created/updated"""
    if instance.transaction_type == 'EXPENSE' and instance.expense_category:
        # Find active budgets for this category
        from django.utils import timezone
        current_date = timezone.now().date()

        budgets = Budget.objects.filter(
            farmer=instance.farmer,
            category=instance.expense_category,
            start_date__lte=current_date,
            end_date__gte=current_date,
            is_active=True
        )

        for budget in budgets:
            # Calculate total spent for this budget period
            from django.db.models import Sum
            spent = Transaction.objects.filter(
                farmer=budget.farmer,
                transaction_type='EXPENSE',
                expense_category=budget.category,
                transaction_date__date__range=[budget.start_date, budget.end_date]
            ).aggregate(total=Sum('amount'))['total'] or 0

            budget.spent_amount = spent
            budget.save()


@receiver(post_delete, sender=Transaction)
def update_budget_on_transaction_delete(sender, instance, **kwargs):
    """Update budget spent amount when expense transaction is deleted"""
    if instance.transaction_type == 'EXPENSE' and instance.expense_category:
        from django.utils import timezone
        current_date = timezone.now().date()

        budgets = Budget.objects.filter(
            farmer=instance.farmer,
            category=instance.expense_category,
            start_date__lte=current_date,
            end_date__gte=current_date,
            is_active=True
        )

        for budget in budgets:
            # Recalculate spent amount
            from django.db.models import Sum
            spent = Transaction.objects.filter(
                farmer=budget.farmer,
                transaction_type='EXPENSE',
                expense_category=budget.category,
                transaction_date__date__range=[budget.start_date, budget.end_date]
            ).aggregate(total=Sum('amount'))['total'] or 0

            budget.spent_amount = spent
            budget.save()


def create_default_categories():
    """Create default income and expense categories"""

    # Default expense categories
    expense_categories = [
        ('Seeds', 'Cost of seeds and seedlings'),
        ('Fertilizers', 'Fertilizer and soil amendments'),
        ('Pesticides', 'Pesticides, herbicides, and fungicides'),
        ('Labor', 'Farm labor costs'),
        ('Equipment', 'Farm equipment and tools'),
        ('Fuel', 'Fuel and energy costs'),
        ('Irrigation', 'Water and irrigation costs'),
        ('Transportation', 'Transportation and logistics'),
        ('Storage', 'Storage and warehousing'),
        ('Insurance', 'Crop and equipment insurance'),
        ('Utilities', 'Electricity, phone, internet'),
        ('Maintenance', 'Equipment and facility maintenance'),
        ('Professional Services', 'Veterinary, consulting, legal services'),
        ('Taxes', 'Property taxes and fees'),
        ('Other', 'Miscellaneous expenses'),
    ]

    for name, description in expense_categories:
        ExpenseCategory.objects.get_or_create(
            name=name,
            defaults={'description': description}
        )

    # Default income categories
    income_categories = [
        ('Crop Sales', 'Revenue from crop sales'),
        ('Livestock Sales', 'Revenue from livestock sales'),
        ('Dairy Products', 'Revenue from milk and dairy products'),
        ('Government Subsidies', 'Government subsidies and support'),
        ('Insurance Claims', 'Insurance claim payments'),
        ('Equipment Rental', 'Income from renting out equipment'),
        ('Consulting', 'Income from consulting services'),
        ('Contract Farming', 'Income from contract farming'),
        ('Other Farm Income', 'Other farm-related income'),
        ('Off-Farm Income', 'Non-farm income sources'),
    ]

    for name, description in income_categories:
        IncomeCategory.objects.get_or_create(
            name=name,
            defaults={'description': description}
        )
