from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='產品名稱')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='價格')
    stock = models.IntegerField(verbose_name='庫存')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '產品'
        verbose_name_plural = '產品'

class Customer(models.Model):
    name = models.CharField(max_length=100, verbose_name='客戶名稱')
    email = models.EmailField(verbose_name='電子郵件')
    phone = models.CharField(max_length=20, verbose_name='電話')
    address = models.TextField(verbose_name='地址')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '客户'
        verbose_name_plural = '客户'

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='客户')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='產品')
    quantity = models.IntegerField(verbose_name='數量')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='總價')
    order_date = models.DateTimeField(auto_now_add=True, verbose_name='訂單日期')
    status = models.CharField(max_length=20, choices=[
        ('pending', '待處理'),
        ('completed', '已完成'),
        ('cancelled', '已取消')
    ], default='pending', verbose_name='狀態')

    def __str__(self):
        return f'{self.customer.name} - {self.product.name}'

    class Meta:
        verbose_name = '訂單'
        verbose_name_plural = '訂單'
