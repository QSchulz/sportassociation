from django.contrib import admin
from .models import (FinancialOperation, CashRegister, TreasuryOperation)

admin.site.register(FinancialOperation)
admin.site.register(CashRegister)
admin.site.register(TreasuryOperation)
