from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('200.00'))

    def __str__(self):
        return f"{self.user.username}'s Account"

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return f"{self.amount} on {self.timestamp} by {self.user.username}"