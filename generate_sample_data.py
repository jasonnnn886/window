import pandas as pd
from datetime import datetime, timedelta
import random
from faker import Faker

# 初始化Faker中文本地化
fake = Faker('zh_CN')

daily_products = [
    '洗衣液', '卫生纸', '洗发水', '沐浴露', '牙膏',
    '洗洁精', '垃圾袋', '保鲜膜', '厨房纸巾', '洗衣粉'
]

# 生成产品数据
def generate_products(num_products=10):
    products = []
    # 确保每个产品只使用一次
    available_products = daily_products.copy()
    for i in range(min(num_products, len(available_products))):
        product_name = available_products.pop(random.randint(0, len(available_products)-1))
        product = {
            'name': product_name,
            'price': round(random.uniform(100, 1000), 2),
            'stock': random.randint(10, 100)
        }
        products.append(product)
    return pd.DataFrame(products)

# 生成客户数据
def generate_customers(num_customers=5):
    customers = []
    for i in range(num_customers):
        customer = {
            'name': fake.unique.name(),
            'email': f'customer{i+1}@example.com',
            'phone': f'1{random.randint(300000000, 399999999)}',
            'address': fake.address()
        }
        customers.append(customer)
    return pd.DataFrame(customers)

# 生成订单数据
def generate_orders(products_df, customers_df, num_orders=20):
    orders = []
    status_choices = ['pending', 'completed', 'cancelled']
    
    for i in range(num_orders):
        product = products_df.iloc[random.randint(0, len(products_df)-1)]
        customer = customers_df.iloc[random.randint(0, len(customers_df)-1)]
        quantity = random.randint(1, 5)
        
        order = {
            'customer_email': customer['email'],
            'customer_phone': customer['phone'],
            'product_name': product['name'],
            'quantity': quantity,
            'total_price': round(quantity * product['price'], 2),
            'status': random.choice(status_choices)
        }
        orders.append(order)
    return pd.DataFrame(orders)

# 生成示例数据并保存到Excel文件
def generate_sample_data(output_file='sample_data.xlsx'):
    # 生成数据
    products_df = generate_products()
    customers_df = generate_customers()
    orders_df = generate_orders(products_df, customers_df)
    
    # 保存到Excel文件
    with pd.ExcelWriter(output_file) as writer:
        products_df.to_excel(writer, sheet_name='products', index=False)
        customers_df.to_excel(writer, sheet_name='customers', index=False)
        orders_df.to_excel(writer, sheet_name='orders', index=False)

if __name__ == '__main__':
    generate_sample_data()
    print('示例数据已生成到sample_data.xlsx文件中')