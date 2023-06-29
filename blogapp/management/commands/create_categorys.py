from typing import Optional, Any

from django.core.management import BaseCommand

from blogapp.models import Category

class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        self.stdout.write('Create category')
        categorys_data = [
            'Технологии',
            'IT и программирование',
        ]
        tags = [
            Category(name=name)
            for name in categorys_data
        ]
        Category.objects.bulk_create(tags)

        self.stdout.write('Done')