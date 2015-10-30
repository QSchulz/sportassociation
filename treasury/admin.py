from django.contrib import admin
from .models import (FinancialOperation, CashRegister, TreasuryOperation)
from management.admin import AdminFileInline

@admin.register(FinancialOperation)
class FinancialOperationAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'description', 'processed_date', 'creation_date',
            'modification_date', 'unregistered_user', 'registered_user',)
    search_fields = ('name', 'description',)
    list_filter = ('creation_date', 'modification_date', 'processed_date',)
    ordering = ('-creation_date',)
    fields = ('name', 'amount', 'description', 'processed_date',
            'unregistered_user', 'registered_user', 'related_activity',)
    inlines = [AdminFileInline,]

    class Media:
        js = ('tinymce/tinymce.min.js', 'js/tinymce_4_config.js')

@admin.register(TreasuryOperation)
class TreasuryOperationAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'description', 'creation_date',
            'modification_date',)
    search_fields = ('name', 'description',)
    list_filter = ('creation_date', 'modification_date',)
    ordering = ('-creation_date',)
    fields = ('name', 'amount', 'cash_register', 'description',)

    class Media:
        js = ('tinymce/tinymce.min.js', 'js/tinymce_4_config.js')

@admin.register(CashRegister)
class CashRegisterAdmin(admin.ModelAdmin):
    list_display = ('name', 'creation_date', 'modification_date',)
    search_fields = ('name',)
    list_filter = ('creation_date', 'modification_date',)
    ordering = ('-creation_date',)
