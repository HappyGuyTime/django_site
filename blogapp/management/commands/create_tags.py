from typing import Optional, Any

from django.core.management import BaseCommand

from blogapp.models import Tag

class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        self.stdout.write('Create tags')
        tags_data = [
            'Искусственный интеллект',
            'Робототехника',
            'Блокчейн',
            'Интернет вещей',
            'Кибербезопасность',
            'Биг-дата',
            'Облачные вычисления',
            'Виртуальная реальность',
            'Расширенная реальность',
            '5G',
            'Веб-разработка',
           ' Мобильная разработка',
            'Искусственный интеллект',
           ' Базы данных',
           ' Компьютерная графика',
            'Машинное обучение',
            'Большие данные',
            'Кибербезопасность',
            'Алгоритмы',
            'DevOps',
        ]
        tags = [
            Tag(name=name)
            for name in tags_data
        ]
        Tag.objects.bulk_create(tags)

        self.stdout.write('Done')