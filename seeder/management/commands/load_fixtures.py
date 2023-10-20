from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        call_command('makemigrations')
        call_command('migrate')
        call_command('loaddata', 'db_users_fixture.json')
        call_command('loaddata', 'db_category_fixture.json')
        call_command('loaddata', 'db_producttype_fixture.json')
        call_command('loaddata', 'db_brand_fixture.json')
        call_command('loaddata', 'db_product_fixture.json')
        call_command('loaddata', 'db_productinventory_fixture.json')
        call_command('loaddata', 'db_product_attribute_fixture.json')
        call_command('loaddata', 'db_product_attribute_value_fixture.json')
        call_command(
            'loaddata', 'db_productinventory_attribute_values_fixture.json')
        call_command('loaddata', 'db_media_fixture.json')
        call_command('loaddata', 'db_stock_fixture.json')
