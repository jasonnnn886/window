from django.core.management.base import BaseCommand
from data_manager.data_processor import process_data
from data_manager.models import Product, Customer, Order

class Command(BaseCommand):
    help = '导入或导出Excel数据文件'

    def add_arguments(self, parser):
        # 添加子命令
        subparsers = parser.add_subparsers(dest='command', help='可用的命令：import - 导入数据, export - 导出数据, clear - 清空数据')

        # 导入数据的子命令
        import_parser = subparsers.add_parser('import', help='从Excel文件导入数据')
        import_parser.add_argument('file', type=str, help='Excel文件路径')
        import_parser.add_argument('--sheet', type=str, choices=['products', 'customers', 'orders'], help='指定要导入的工作表名称')
        import_parser.add_argument('--export', type=str, help='同时将数据导出到指定Excel文件')

        # 导出数据的子命令
        export_parser = subparsers.add_parser('export', help='导出数据到Excel文件')
        export_parser.add_argument('file', type=str, help='Excel文件路径')

        # 清理数据的子命令
        clear_parser = subparsers.add_parser('clear', help='清空所有数据')
        clear_parser.add_argument('--confirm', action='store_true', help='确认删除操作')

        # 添加通用帮助信息
        parser.description = '''数据处理命令行工具

示例:
  python manage.py process_data import data.xlsx            # 导入所有数据
  python manage.py process_data import data.xlsx --sheet products  # 仅导入产品数据
  python manage.py process_data export output.xlsx         # 导出所有数据
  python manage.py process_data clear --confirm            # 清空所有数据'''

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
                success, message = True, "数据清除完成"
            else:
                self.stdout.write(self.style.WARNING('请添加--confirm参数确认执行删除'))
                return

        if success:
            self.stdout.write(self.style.SUCCESS(message))
        else:
            self.stdout.write(self.style.ERROR(message))