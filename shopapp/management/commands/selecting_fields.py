from typing import Optional, Any

from django.core.management import BaseCommand
from django.contrib.auth.models import User

from shopapp.models import Product

class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        self.stdout.write('Start demo fields')

        # users_info = User.objects.values_list('pk', 'username')
        users_info = User.objects.values_list('username', flat=True)
        for user_info in users_info:
            print(user_info)

        # products_values = Product.objects.values('pk', 'name')
        # for p_value in products_values:
        #     print(p_value)

        self.stdout.write('Done')