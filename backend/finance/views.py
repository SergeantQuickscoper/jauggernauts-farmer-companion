from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from django.db import transaction

from .models import (
    FinanceAccount, Transaction, ExpenseCategory, IncomeCategory,
    Budget, CropFinance, FinancialGoal
)
from .serializers import (
    FinanceAccountSerializer, TransactionSerializer, ExpenseCategorySerializer,
    IncomeCategorySerializer, BudgetSerializer, CropFinanceSerializer,
    FinancialGoalSerializer, TransactionCreateSerializer, BudgetCreateSerializer
)


class FinanceAccountViewSet(viewsets.ModelViewSet):
    """ViewSet for managing finance accounts"""
    serializer_class = FinanceAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FinanceAccount.objects.filter(farmer=self.request.user, is_active=True)

    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)

    @action(detail=True, methods=['post'])
    def update_balance(self, request, pk=None):
        """Manually update account balance"""
        account = self.get_object()
        new_balance = request.data.get('balance')

        if new_balance is not None:
            try:
                account.current_balance = Decimal(str(new_balance))
                account.save()
                return Response({
                    'message': 'Balance updated successfully',
                    'new_balance': account.current_balance
                })
            except (ValueError, TypeError):
                return Response(
                    {'error': 'Invalid balance amount'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(
            {'error': 'Balance amount is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['get'])
    def total_balance(self, request):
        """Get total balance across all accounts"""
        total = self.get_queryset().aggregate(
            total=Sum('current_balance')
        )['total'] or Decimal('0.00')

        return Response({'total_balance': total})


class TransactionViewSet(viewsets.ModelViewSet):
    """ViewSet for managing transactions"""
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TransactionCreateSerializer
        return TransactionSerializer

    def get_queryset(self):
        queryset = Transaction.objects.filter(farmer=self.request.user)

        # Filter by transaction type
        transaction_type = self.request.query_params.get('type')
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type.upper())

        # Filter by account
        account_id = self.request.query_params.get('account')
        if account_id:
            queryset = queryset.filter(account_id=account_id)

        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                queryset = queryset.filter(transaction_date__gte=start_date)
            except ValueError:
                pass

        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                queryset = queryset.filter(transaction_date__lte=end_date)
            except ValueError:
                pass

        return queryset

    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get transaction summary"""
        queryset = self.get_queryset()

        # Get date range (default to current month)
        end_date = timezone.now().date()
        start_date = end_date.replace(day=1)

        start_param = request.query_params.get('start_date')
        end_param = request.query_params.get('end_date')

        if start_param:
            try:
                start_date = datetime.strptime(start_param, '%Y-%m-%d').date()
            except ValueError:
                pass

        if end_param:
            try:
                end_date = datetime.strptime(end_param, '%Y-%m-%d').date()
            except ValueError:
                pass

        # Filter by date range
        period_transactions = queryset.filter(
            transaction_date__date__range=[start_date, end_date]
        )

        # Calculate totals
        income = period_transactions.filter(
            transaction_type='INCOME'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

        expense = period_transactions.filter(
            transaction_type='EXPENSE'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

        net_flow = income - expense

        # Category-wise breakdown
        expense_by_category = period_transactions.filter(
            transaction_type='EXPENSE'
        ).values('expense_category__name').annotate(
            total=Sum('amount')
        ).order_by('-total')

        income_by_category = period_transactions.filter(
            transaction_type='INCOME'
        ).values('income_category__name').annotate(
            total=Sum('amount')
        ).order_by('-total')

        return Response({
            'period': {
                'start_date': start_date,
                'end_date': end_date
            },
            'summary': {
                'total_income': income,
                'total_expense': expense,
                'net_cash_flow': net_flow,
                'transaction_count': period_transactions.count()
            },
            'expense_by_category': expense_by_category,
            'income_by_category': income_by_category
        })

    @action(detail=False, methods=['post'])
    def transfer(self, request):
        """Transfer money between accounts"""
        from_account_id = request.data.get('from_account')
        to_account_id = request.data.get('to_account')
        amount = request.data.get('amount')
        description = request.data.get('description', 'Account transfer')

        if not all([from_account_id, to_account_id, amount]):
            return Response(
                {'error': 'from_account, to_account, and amount are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            from_account = FinanceAccount.objects.get(
                id=from_account_id, farmer=request.user
            )
            to_account = FinanceAccount.objects.get(
                id=to_account_id, farmer=request.user
            )
            amount = Decimal(str(amount))

            if amount <= 0:
                return Response(
                    {'error': 'Amount must be positive'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            if from_account.current_balance < amount:
                return Response(
                    {'error': 'Insufficient balance'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create transfer transaction
            with transaction.atomic():
                transfer_transaction = Transaction.objects.create(
                    farmer=request.user,
                    account=from_account,
                    to_account=to_account,
                    transaction_type='TRANSFER',
                    amount=amount,
                    description=description,
                    transaction_date=timezone.now()
                )

            return Response({
                'message': 'Transfer completed successfully',
                'transaction_id': transfer_transaction.id,
                'from_account_balance': from_account.current_balance,
                'to_account_balance': to_account.current_balance
            })

        except FinanceAccount.DoesNotExist:
            return Response(
                {'error': 'Invalid account'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except (ValueError, TypeError):
            return Response(
                {'error': 'Invalid amount'}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class ExpenseCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for expense categories"""
    serializer_class = ExpenseCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ExpenseCategory.objects.filter(is_active=True)


class IncomeCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for income categories"""
    serializer_class = IncomeCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return IncomeCategory.objects.filter(is_active=True)


class BudgetViewSet(viewsets.ModelViewSet):
    """ViewSet for managing budgets"""
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BudgetCreateSerializer
        return BudgetSerializer

    def get_queryset(self):
        return Budget.objects.filter(farmer=self.request.user, is_active=True)

    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)

    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current active budgets"""
        current_date = timezone.now().date()
        current_budgets = self.get_queryset().filter(
            start_date__lte=current_date,
            end_date__gte=current_date
        )

        # Update spent amounts
        for budget in current_budgets:
            spent = Transaction.objects.filter(
                farmer=request.user,
                transaction_type='EXPENSE',
                expense_category=budget.category,
                transaction_date__date__range=[budget.start_date, budget.end_date]
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

            budget.spent_amount = spent
            budget.save()

        serializer = self.get_serializer(current_budgets, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def spending_analysis(self, request, pk=None):
        """Get detailed spending analysis for a budget"""
        budget = self.get_object()

        transactions = Transaction.objects.filter(
            farmer=request.user,
            transaction_type='EXPENSE',
            expense_category=budget.category,
            transaction_date__date__range=[budget.start_date, budget.end_date]
        ).order_by('-transaction_date')

        serializer = TransactionSerializer(transactions, many=True)

        return Response({
            'budget': BudgetSerializer(budget).data,
            'transactions': serializer.data,
            'analysis': {
                'daily_average': budget.spent_amount / max((timezone.now().date() - budget.start_date).days, 1),
                'remaining_days': max((budget.end_date - timezone.now().date()).days, 0),
                'projected_spending': budget.spent_amount + (budget.spent_amount / max((timezone.now().date() - budget.start_date).days, 1)) * max((budget.end_date - timezone.now().date()).days, 0)
            }
        })


class CropFinanceViewSet(viewsets.ModelViewSet):
    """ViewSet for managing crop finances"""
    serializer_class = CropFinanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = CropFinance.objects.filter(farmer=self.request.user)

        # Filter by year
        year = self.request.query_params.get('year')
        if year:
            try:
                queryset = queryset.filter(year=int(year))
            except ValueError:
                pass

        # Filter by season
        season = self.request.query_params.get('season')
        if season:
            queryset = queryset.filter(season__icontains=season)

        # Filter by crop
        crop = self.request.query_params.get('crop')
        if crop:
            queryset = queryset.filter(crop_name__icontains=crop)

        return queryset

    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)

    @action(detail=False, methods=['get'])
    def profitability_analysis(self, request):
        """Analyze crop profitability"""
        queryset = self.get_queryset()

        # Overall stats
        total_crops = queryset.count()
        profitable_crops = queryset.filter(total_revenue__gt=0).count()

        # Aggregate totals
        totals = queryset.aggregate(
            total_investment=Sum('seed_cost') + Sum('fertilizer_cost') + Sum('pesticide_cost') + 
                           Sum('labor_cost') + Sum('irrigation_cost') + Sum('equipment_cost') + Sum('other_costs'),
            total_revenue=Sum('total_revenue')
        )

        total_investment = totals['total_investment'] or Decimal('0.00')
        total_revenue = totals['total_revenue'] or Decimal('0.00')
        overall_profit = total_revenue - total_investment

        # Best performing crops
        best_crops = []
        for crop in queryset:
            if crop.total_investment > 0:
                best_crops.append({
                    'id': crop.id,
                    'crop_name': crop.crop_name,
                    'season': crop.season,
                    'year': crop.year,
                    'profit': crop.profit_loss,
                    'roi_percentage': crop.roi_percentage,
                    'investment': crop.total_investment,
                    'revenue': crop.total_revenue
                })

        best_crops.sort(key=lambda x: x['roi_percentage'], reverse=True)

        # Crop-wise summary
        crop_summary = {}
        for crop in queryset:
            crop_name = crop.crop_name
            if crop_name not in crop_summary:
                crop_summary[crop_name] = {
                    'total_seasons': 0,
                    'total_investment': Decimal('0.00'),
                    'total_revenue': Decimal('0.00'),
                    'total_area': Decimal('0.00')
                }

            summary = crop_summary[crop_name]
            summary['total_seasons'] += 1
            summary['total_investment'] += crop.total_investment
            summary['total_revenue'] += crop.total_revenue
            summary['total_area'] += crop.area_acres

        # Calculate average ROI per crop
        for crop_name, summary in crop_summary.items():
            if summary['total_investment'] > 0:
                summary['avg_roi'] = ((summary['total_revenue'] - summary['total_investment']) / summary['total_investment']) * 100
                summary['profit_per_acre'] = (summary['total_revenue'] - summary['total_investment']) / summary['total_area'] if summary['total_area'] > 0 else 0
            else:
                summary['avg_roi'] = 0
                summary['profit_per_acre'] = 0

        return Response({
            'overall_stats': {
                'total_crops': total_crops,
                'profitable_crops': profitable_crops,
                'total_investment': total_investment,
                'total_revenue': total_revenue,
                'overall_profit': overall_profit,
                'overall_roi': (overall_profit / total_investment * 100) if total_investment > 0 else 0
            },
            'best_performing': best_crops[:5],
            'crop_wise_summary': crop_summary
        })

    @action(detail=True, methods=['post'])
    def add_sale(self, request, pk=None):
        """Add a sale transaction for this crop"""
        crop_finance = self.get_object()

        amount = request.data.get('amount')
        quantity = request.data.get('quantity')
        price_per_unit = request.data.get('price_per_unit')
        description = request.data.get('description', f'{crop_finance.crop_name} sale')

        if not amount:
            return Response(
                {'error': 'Sale amount is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            amount = Decimal(str(amount))

            # Update crop revenue
            crop_finance.total_revenue += amount
            if quantity:
                crop_finance.actual_yield = Decimal(str(quantity))
            crop_finance.save()

            # Create income transaction if account is specified
            account_id = request.data.get('account_id')
            if account_id:
                try:
                    account = FinanceAccount.objects.get(
                        id=account_id, farmer=request.user
                    )

                    # Get or create crop sales income category
                    income_category, _ = IncomeCategory.objects.get_or_create(
                        name='Crop Sales',
                        defaults={'description': 'Income from crop sales'}
                    )

                    Transaction.objects.create(
                        farmer=request.user,
                        account=account,
                        transaction_type='INCOME',
                        amount=amount,
                        description=description,
                        income_category=income_category,
                        transaction_date=timezone.now()
                    )

                except FinanceAccount.DoesNotExist:
                    pass

            return Response({
                'message': 'Sale recorded successfully',
                'new_revenue': crop_finance.total_revenue,
                'profit_loss': crop_finance.profit_loss
            })

        except (ValueError, TypeError):
            return Response(
                {'error': 'Invalid amount'}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class FinancialGoalViewSet(viewsets.ModelViewSet):
    """ViewSet for managing financial goals"""
    serializer_class = FinancialGoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FinancialGoal.objects.filter(farmer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)

    @action(detail=True, methods=['post'])
    def add_contribution(self, request, pk=None):
        """Add contribution towards a goal"""
        goal = self.get_object()
        amount = request.data.get('amount')

        if not amount:
            return Response(
                {'error': 'Contribution amount is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            amount = Decimal(str(amount))

            if amount <= 0:
                return Response(
                    {'error': 'Amount must be positive'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            goal.current_amount += amount

            # Check if goal is achieved
            if goal.current_amount >= goal.target_amount:
                goal.is_achieved = True

            goal.save()

            return Response({
                'message': 'Contribution added successfully',
                'new_amount': goal.current_amount,
                'remaining': goal.remaining_amount,
                'percentage_achieved': goal.percentage_achieved,
                'is_achieved': goal.is_achieved
            })

        except (ValueError, TypeError):
            return Response(
                {'error': 'Invalid amount'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'])
    def progress_summary(self, request):
        """Get progress summary for all goals"""
        goals = self.get_queryset()

        total_goals = goals.count()
        achieved_goals = goals.filter(is_achieved=True).count()

        # Goals by type
        goals_by_type = {}
        for goal in goals:
            goal_type = goal.get_goal_type_display()
            if goal_type not in goals_by_type:
                goals_by_type[goal_type] = {
                    'count': 0,
                    'total_target': Decimal('0.00'),
                    'total_achieved': Decimal('0.00')
                }

            goals_by_type[goal_type]['count'] += 1
            goals_by_type[goal_type]['total_target'] += goal.target_amount
            goals_by_type[goal_type]['total_achieved'] += goal.current_amount

        # Upcoming deadlines
        upcoming_goals = goals.filter(
            is_achieved=False,
            target_date__gte=timezone.now().date(),
            target_date__lte=timezone.now().date() + timedelta(days=90)
        ).order_by('target_date')

        return Response({
            'summary': {
                'total_goals': total_goals,
                'achieved_goals': achieved_goals,
                'achievement_rate': (achieved_goals / total_goals * 100) if total_goals > 0 else 0
            },
            'goals_by_type': goals_by_type,
            'upcoming_deadlines': FinancialGoalSerializer(upcoming_goals[:5], many=True).data
        })


# Dashboard Views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal

from .models import FinanceAccount, Transaction, Budget, FinancialGoal, CropFinance
from .serializers import DashboardSummarySerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_summary(request):
    """Get finance dashboard summary for the authenticated farmer"""
    farmer = request.user
    current_date = timezone.now().date()
    current_month_start = current_date.replace(day=1)

    # Account balances
    accounts = FinanceAccount.objects.filter(farmer=farmer, is_active=True)
    total_balance = accounts.aggregate(total=Sum('current_balance'))['total'] or Decimal('0.00')

    # Monthly income and expenses
    monthly_transactions = Transaction.objects.filter(
        farmer=farmer,
        transaction_date__date__gte=current_month_start
    )

    monthly_income = monthly_transactions.filter(
        transaction_type='INCOME'
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    monthly_expense = monthly_transactions.filter(
        transaction_type='EXPENSE'
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    net_cash_flow = monthly_income - monthly_expense

    # Budget summary
    active_budgets = Budget.objects.filter(
        farmer=farmer,
        is_active=True,
        start_date__lte=current_date,
        end_date__gte=current_date
    )

    overbudget_count = 0
    for budget in active_budgets:
        if budget.spent_amount > budget.budgeted_amount:
            overbudget_count += 1

    # Goals summary
    active_goals = FinancialGoal.objects.filter(farmer=farmer, is_achieved=False)
    achieved_goals = FinancialGoal.objects.filter(farmer=farmer, is_achieved=True)

    # Recent transactions
    recent_transactions = Transaction.objects.filter(
        farmer=farmer
    ).order_by('-transaction_date')[:5]

    from .serializers import TransactionSerializer

    dashboard_data = {
        'total_balance': total_balance,
        'monthly_income': monthly_income,
        'monthly_expense': monthly_expense,
        'net_cash_flow': net_cash_flow,
        'active_budgets_count': active_budgets.count(),
        'overbudget_count': overbudget_count,
        'active_goals_count': active_goals.count(),
        'achieved_goals_count': achieved_goals.count(),
        'recent_transactions': TransactionSerializer(recent_transactions, many=True).data
    }

    return Response(dashboard_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def monthly_trends(request):
    """Get monthly income/expense trends for the last 12 months"""
    farmer = request.user
    current_date = timezone.now().date()

    # Get last 12 months data
    trends = []
    for i in range(12):
        month_date = current_date - timedelta(days=30*i)
        month_start = month_date.replace(day=1)

        # Get next month's start date
        if month_start.month == 12:
            next_month = month_start.replace(year=month_start.year + 1, month=1)
        else:
            next_month = month_start.replace(month=month_start.month + 1)

        month_transactions = Transaction.objects.filter(
            farmer=farmer,
            transaction_date__date__gte=month_start,
            transaction_date__date__lt=next_month
        )

        income = month_transactions.filter(
            transaction_type='INCOME'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

        expense = month_transactions.filter(
            transaction_type='EXPENSE'
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

        trends.append({
            'month': month_start.strftime('%b %Y'),
            'income': income,
            'expense': expense,
            'net_flow': income - expense
        })

    return Response(trends)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def expense_categories_breakdown(request):
    """Get expense breakdown by categories for the current month"""
    farmer = request.user
    current_date = timezone.now().date()
    current_month_start = current_date.replace(day=1)

    category_expenses = Transaction.objects.filter(
        farmer=farmer,
        transaction_type='EXPENSE',
        transaction_date__date__gte=current_month_start,
        expense_category__isnull=False
    ).values('expense_category__name').annotate(
        total_amount=Sum('amount'),
        transaction_count=Count('id')
    ).order_by('-total_amount')

    # Calculate percentages
    total_expense = sum(item['total_amount'] for item in category_expenses)

    breakdown = []
    for item in category_expenses:
        percentage = (item['total_amount'] / total_expense * 100) if total_expense > 0 else 0
        breakdown.append({
            'category_name': item['expense_category__name'],
            'amount': item['total_amount'],
            'percentage': round(percentage, 2),
            'transaction_count': item['transaction_count']
        })

    return Response(breakdown)
