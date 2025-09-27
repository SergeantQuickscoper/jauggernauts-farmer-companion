# Finance Management Module

This module provides comprehensive financial management capabilities for farmers including:

## Features

### 1. Account Management
- Multiple account types (Savings, Current, Loan, Credit, Cash)
- Real-time balance tracking
- Account balance updates with transactions

### 2. Transaction Management
- Income, Expense, and Transfer transactions
- Category-wise transaction tracking
- Receipt image uploads
- Detailed transaction history with filters

### 3. Budget Management
- Category-wise budget planning
- Real-time budget vs actual spending tracking
- Budget alerts and notifications
- Period-based budget analysis

### 4. Crop Finance Tracking
- Season-wise crop investment tracking
- Detailed cost breakdown (seeds, fertilizers, labor, etc.)
- Revenue and profit/loss calculations
- ROI analysis per crop

### 5. Financial Goals
- Savings goals and targets
- Progress tracking
- Achievement notifications
- Goal type categorization

### 6. Dashboard & Analytics
- Financial summary dashboard
- Monthly trends analysis
- Category-wise spending breakdown
- Profitability analysis

## API Endpoints

### Accounts
- `GET /api/finance/accounts/` - List all accounts
- `POST /api/finance/accounts/` - Create new account
- `GET /api/finance/accounts/{id}/` - Get account details
- `PUT /api/finance/accounts/{id}/` - Update account
- `POST /api/finance/accounts/{id}/update_balance/` - Manually update balance
- `GET /api/finance/accounts/total_balance/` - Get total balance across accounts

### Transactions
- `GET /api/finance/transactions/` - List transactions (with filters)
- `POST /api/finance/transactions/` - Create new transaction
- `GET /api/finance/transactions/summary/` - Get transaction summary
- `POST /api/finance/transactions/transfer/` - Transfer between accounts

### Budgets
- `GET /api/finance/budgets/` - List budgets
- `POST /api/finance/budgets/` - Create new budget
- `GET /api/finance/budgets/current/` - Get current active budgets
- `GET /api/finance/budgets/{id}/spending_analysis/` - Get spending analysis

### Crop Finances
- `GET /api/finance/crop-finances/` - List crop finances
- `POST /api/finance/crop-finances/` - Create new crop finance record
- `GET /api/finance/crop-finances/profitability_analysis/` - Profitability analysis
- `POST /api/finance/crop-finances/{id}/add_sale/` - Add crop sale

### Financial Goals
- `GET /api/finance/financial-goals/` - List goals
- `POST /api/finance/financial-goals/` - Create new goal
- `POST /api/finance/financial-goals/{id}/add_contribution/` - Add contribution
- `GET /api/finance/financial-goals/progress_summary/` - Progress summary

### Dashboard
- `GET /api/finance/dashboard/summary/` - Dashboard summary
- `GET /api/finance/dashboard/trends/` - Monthly trends
- `GET /api/finance/dashboard/expense-breakdown/` - Expense breakdown

## Setup Instructions

1. Make sure PostgreSQL is installed and running
2. Install required packages: `pip install -r requirements.txt`
3. Run migrations: `python manage.py makemigrations finance && python manage.py migrate`
4. Create superuser: `python manage.py createsuperuser`
5. Populate default categories: `python manage.py populate_categories`
6. Start development server: `python manage.py runserver`

## Usage Examples

### Creating a Transaction
```python
POST /api/finance/transactions/
{
    "account": 1,
    "transaction_type": "EXPENSE",
    "amount": "500.00",
    "description": "Bought seeds for wheat",
    "expense_category": 1,
    "transaction_date": "2024-01-15T10:30:00Z"
}
```

### Creating a Budget
```python
POST /api/finance/budgets/
{
    "name": "Monthly Fertilizer Budget",
    "category": 2,
    "budgeted_amount": "5000.00",
    "start_date": "2024-01-01",
    "end_date": "2024-01-31"
}
```

### Transfer Between Accounts
```python
POST /api/finance/transactions/transfer/
{
    "from_account": 1,
    "to_account": 2,
    "amount": "1000.00",
    "description": "Transfer to savings"
}
```

## Models

- **FinanceAccount**: User's financial accounts
- **Transaction**: All financial transactions
- **ExpenseCategory**: Categories for expenses
- **IncomeCategory**: Categories for income
- **Budget**: Budget planning and tracking
- **CropFinance**: Crop-wise financial tracking
- **FinancialGoal**: Financial goals and targets

## Admin Interface

The module includes a comprehensive Django admin interface for:
- Managing categories
- Viewing and editing transactions
- Monitoring budgets and goals
- Generating reports

## Security Features

- User-based data isolation
- Token-based authentication
- Input validation and sanitization
- Balance integrity checks
- Transaction rollback on errors
