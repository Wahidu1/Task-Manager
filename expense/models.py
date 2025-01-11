from django.db import models
from account.models import BaseModel

class Expense(BaseModel):
    payment_method_choices = [
            ('credit_card', 'Credit Card'),
            ('debit_card', 'Debit Card'),
            ('paypal', 'PayPal'),
            ('bank_transfer', 'Bank Transfer'),
            ('cash', 'Cash'),
        ]
    recurrence_choices = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually'),
    ]
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    payment_method = models.CharField(max_length=50, choices=payment_method_choices, blank=True, null=True)
    date = models.DateTimeField()
    recurring = models.BooleanField(default=False)
    recurrence_period = models.CharField(max_length=50, choices=recurrence_choices, default="daily")
    tags = models.CharField(max_length=50) 
    
