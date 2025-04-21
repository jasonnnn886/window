from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='产品名称')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    stock = models.IntegerField(verbose_name='库存')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '产品'
        verbose_name_plural = '产品'

class Customer(models.Model):
    name = models.CharField(max_length=100, verbose_name='客户名称')
    email = models.EmailField(verbose_name='电子邮件')
    phone = models.CharField(max_length=20, verbose_name='电话')
    address = models.TextField(verbose_name='地址')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '客户'
        verbose_name_plural = '客户'

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='客户')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='产品')
    quantity = models.IntegerField(verbose_name='数量')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='总价')
    order_date = models.DateTimeField(auto_now_add=True, verbose_name='订单日期')
    status = models.CharField(max_length=20, choices=[
        ('pending', '待处理'),
        ('completed', '已完成'),
        ('cancelled', '已取消')
    ], default='pending', verbose_name='状态')

    def __str__(self):
        return f'{self.customer.name} - {self.product.name}'

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = '订单'
