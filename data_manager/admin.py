from django.contrib import admin
from django.http import HttpResponse
from .models import Product, Customer, Order
from .data_processor import export_data
import tempfile
import os

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'price')
    search_help_text = "輸入產品名稱進行搜尋"
    actions = ['export_to_excel']
    
    def export_to_excel(self, request, queryset):
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=data_export.xlsx'
        export_data(response)
        return response
    export_to_excel.short_description = '匯出資料到Excel'

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at')
    search_fields = ('name', 'email', 'phone', 'address')
    list_filter = ('created_at',)
    search_help_text = "輸入客戶名稱、電子郵件、電話或地址進行搜尋"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'quantity', 'total_price', 'order_date', 'status')
    search_fields = ('customer__name', 'product__name', 'status', 'total_price')
    list_filter = ('status', 'order_date')
    search_help_text = "輸入客戶名稱、產品名稱、狀態或總價進行搜尋"