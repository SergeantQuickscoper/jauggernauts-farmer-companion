from django.core.management.base import BaseCommand
from finance.models import ExpenseCategory, IncomeCategory


class Command(BaseCommand):
    help = 'Populate default expense and income categories for finance management'

    def handle(self, *args, **options):
        self.stdout.write('Creating default expense categories...')

        # Default expense categories for farming
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
            ('Marketing', 'Marketing and advertising expenses'),
            ('Packaging', 'Packaging and processing costs'),
            ('Other', 'Miscellaneous expenses'),
        ]

        created_expense_count = 0
        for name, description in expense_categories:
            category, created = ExpenseCategory.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )
            if created:
                created_expense_count += 1
                self.stdout.write(f'Created expense category: {name}')

        self.stdout.write('Creating default income categories...')

        # Default income categories for farming
        income_categories = [
            ('Crop Sales', 'Revenue from crop sales'),
            ('Livestock Sales', 'Revenue from livestock sales'),
            ('Dairy Products', 'Revenue from milk and dairy products'),
            ('Poultry Products', 'Revenue from eggs and poultry'),
            ('Government Subsidies', 'Government subsidies and support payments'),
            ('Insurance Claims', 'Insurance claim payments'),
            ('Equipment Rental', 'Income from renting out equipment'),
            ('Land Rental', 'Income from renting out land'),
            ('Consulting', 'Income from agricultural consulting services'),
            ('Contract Farming', 'Income from contract farming agreements'),
            ('Value-Added Products', 'Income from processed farm products'),
            ('Agri-Tourism', 'Income from farm tourism activities'),
            ('Other Farm Income', 'Other farm-related income sources'),
            ('Off-Farm Income', 'Non-farm income sources'),
        ]

        created_income_count = 0
        for name, description in income_categories:
            category, created = IncomeCategory.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )
            if created:
                created_income_count += 1
                self.stdout.write(f'Created income category: {name}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_expense_count} expense categories and {created_income_count} income categories'
            )
        )
