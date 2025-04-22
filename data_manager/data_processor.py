import pandas as pd
from django.core.management.base import BaseCommand
from decimal import Decimal
from datetime import datetime
from data_manager.models import Product, Customer, Order

def clean_data(df, model_type):
    """清理和驗證數據"""
    # 刪除空行
    df = df.dropna(how='all')
    # 數據去重
    df = df.drop_duplicates()
    # 格式校驗
    if model_type == 'order':
        if 'order_date' in df.columns:
            df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
        else:
            df['order_date'] = datetime.now()
    # 填充缺失值
    df = df.fillna({'status': 'pending'})
    return df

def format_data(df, model_type):
    """格式化數據以匹配Django模型"""
    if model_type == 'product':
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df['stock'] = pd.to_numeric(df['stock'], errors='coerce')
    elif model_type == 'order':
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
        df['total_price'] = pd.to_numeric(df['total_price'], errors='coerce')
    return df

def import_products(file_path):
    """導入產品數據"""
    df = pd.read_excel(file_path, sheet_name='products')
    df = clean_data(df, 'product')
    df = format_data(df, 'product')
    # 對產品數據進行去重處理
    df = df.drop_duplicates(subset=['name'])
    
    for _, row in df.iterrows():
        # 使用filter().first()替代get()來避免重複產品的問題
        existing_product = Product.objects.filter(name=row['name']).first()
        if existing_product:
            # 更新現有產品的資訊
            existing_product.price = Decimal(str(row['price']))
            existing_product.stock = int(row['stock'])
            existing_product.save()
        else:
            # 創建新產品
            Product.objects.create(
                name=row['name'],
                price=Decimal(str(row['price'])),
                stock=int(row['stock'])
            )

def import_customers(file_path):
    """導入客戶數據"""
    df = pd.read_excel(file_path, sheet_name='customers')
    df = clean_data(df, 'customer')
    df = df.drop_duplicates(subset=['email', 'phone'])
    
    for _, row in df.iterrows():
        customer, created = Customer.objects.get_or_create(
            email=row['email'],
            phone=row['phone'],
            defaults={
                'name': row['name'],
                'address': row['address']
            }
        )

def import_orders(file_path):
    """導入訂單數據"""
    df = pd.read_excel(file_path, sheet_name='orders')
    df = clean_data(df, 'order')
    df = format_data(df, 'order')
    
    for _, row in df.iterrows():
        # 使用email和phone作為唯一標識符查詢客戶
        customer = Customer.objects.get(email=row['customer_email'], phone=row['customer_phone'])
        product = Product.objects.get(name=row['product_name'])
        
        Order.objects.create(
            customer=customer,
            product=product,
            quantity=int(row['quantity']),
            total_price=Decimal(str(row['total_price'])),
            status=row['status']
        )

def export_data(output):
    """導出所有數據到Excel
    
    Args:
        output: 可以是檔案路徑或HttpResponse對象
    """
    # 導出產品數據
    products_data = [{
        'name': p.name,
        'price': float(p.price),
        'stock': p.stock,
        'created_at': p.created_at.replace(tzinfo=None)
    } for p in Product.objects.all()]
    products_df = pd.DataFrame(products_data)
    
    # 導出客戶數據
    customers_data = [{
        'name': c.name,
        'email': c.email,
        'phone': c.phone,
        'address': c.address,
        'created_at': c.created_at.replace(tzinfo=None)
    } for c in Customer.objects.all()]
    customers_df = pd.DataFrame(customers_data)
    
    # 導出訂單數據
    orders_data = [{
        'customer_name': o.customer.name,
        'customer_email': o.customer.email,
        'customer_phone': o.customer.phone,
        'product_name': o.product.name,
        'quantity': o.quantity,
        'total_price': float(o.total_price),
        'order_date': o.order_date.replace(tzinfo=None),
        'status': o.status
    } for o in Order.objects.all()]
    orders_df = pd.DataFrame(orders_data)
    
    # 創建Excel寫入器
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        products_df.to_excel(writer, sheet_name='products', index=False)
        customers_df.to_excel(writer, sheet_name='customers', index=False)
        orders_df.to_excel(writer, sheet_name='orders', index=False)

def process_data(input_file, output_file=None, sheet_to_import=None):
    """處理數據的主函數"""
    try:
        messages = []
        
        # 如果提供了輸入檔案，則進行導入
        if input_file:
            # 檢查Excel檔案中是否包含所需的工作表
            excel_file = pd.ExcelFile(input_file)
            required_sheets = ['products', 'customers', 'orders']
            if sheet_to_import:
                required_sheets = [sheet_to_import]
            missing_sheets = [sheet for sheet in required_sheets if sheet not in excel_file.sheet_names]
            if missing_sheets:
                return False, f"Excel檔案缺少以下工作表：{', '.join(missing_sheets)}"
            
            # 按順序導入數據
            if 'products' in required_sheets:
                try:
                    import_products(input_file)
                    messages.append("產品數據導入成功")
                except Exception as e:
                    return False, f"產品數據導入失敗: {str(e)}"
            if 'customers' in required_sheets:
                try:
                    import_customers(input_file)
                    messages.append("客戶數據導入成功")
                except Exception as e:
                    return False, f"客戶數據導入失敗: {str(e)}"
            if 'orders' in required_sheets:
                try:
                    import_orders(input_file)
                    messages.append("訂單數據導入成功")
                except Exception as e:
                    return False, f"訂單數據導入失敗: {str(e)}"
        
        # 如果指定了輸出檔案，則導出數據
        if output_file:
            try:
                export_data(output_file)
                messages.append("數據導出成功")
            except Exception as e:
                return False, f"數據導出失敗: {str(e)}"
        
        return True, "\n".join(messages) if messages else "操作完成"
    except Exception as e:
        return False, f"數據處理失敗: {str(e)}"