from django.core.management.base import BaseCommand
from data_manager.data_processor import process_data
from data_manager.models import Product, Customer, Order

class Command(BaseCommand):
    help = '導入或導出Excel數據文件'

    def add_arguments(self, parser):
        # 添加子命令
        subparsers = parser.add_subparsers(dest='command', help='可用命令：import - 導入數據, export - 導出數據, clear - 清空數據')

        # 導入數據的子命令
        import_parser = subparsers.add_parser('import', help='從Excel文件導入數據')
        import_parser.add_argument('file', type=str, help='Excel文件路徑')
        import_parser.add_argument('--sheet', type=str, choices=['products', 'customers', 'orders'], help='指定要導入的工作表名稱')
        import_parser.add_argument('--export', type=str, help='同時將數據導出到指定Excel文件')

        # 導出數據的子命令
        export_parser = subparsers.add_parser('export', help='導出數據到Excel文件')
        export_parser.add_argument('file', type=str, help='Excel文件路徑')

        # 清理數據的子命令
        clear_parser = subparsers.add_parser('clear', help='清空所有數據')
        clear_parser.add_argument('--confirm', action='store_true', help='確認刪除操作')

        # 添加通用幫助信息
        parser.description = '''數據處理命令行工具

示例:
  python manage.py process_data import data.xlsx            # 導入所有數據
  python manage.py process_data import data.xlsx --sheet products  # 僅導入產品數據
  python manage.py process_data export output.xlsx         # 導出所有數據
  python manage.py process_data clear --confirm            # 清空所有數據'''

    def handle(self, *args, **options):
        command = options['command']
        if command == 'import':
            success, message = process_data(
                options['file'],
                output_file=options.get('export'),
                sheet_to_import=options.get('sheet')
            )
        elif command == 'export':
            file_path = options['file']
            success, message = process_data(None, file_path)
        elif command == 'clear':
            if options['confirm']:
                Product.objects.all().delete()
                Customer.objects.all().delete()
                Order.objects.all().delete()
                success, message = True, "所有數據已清空"
            else:
                self.stdout.write(self.style.WARNING('請添加--confirm參數確認執行刪除'))
                return

        if success:
            self.stdout.write(self.style.SUCCESS(message))
        else:
            self.stdout.write(self.style.ERROR(message))