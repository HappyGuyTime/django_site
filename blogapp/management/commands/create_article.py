from typing import Optional, Any

from django.core.management import BaseCommand
from django.db import transaction

from blogapp.models import Author, Article, Tag, Category

class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        self.stdout.write('Create Article')

        author = Author.objects.get(name='Joan')
        category = Category.objects.get(name='IT и программирование')
        tags = Tag.objects.filter(id__gte=10)
        article, created = Article.objects.get_or_create(
            title='Машинное обучение: Изменение парадигмы в IT и программировании',
            content='IT и программирование являются одними из самых динамичных и инновационных областей современного мира. Однако, с появлением машинного обучения (Machine Learning, ML), мы наблюдаем революцию в способах, которыми компьютеры могут "учиться" и принимать решения. В этой статье мы рассмотрим, как машинное обучение меняет парадигму в IT и программировании, и как его применение открывает новые возможности для разработчиков.',
            author=author,
            category=category,
        )
        for tag in tags:
           article.tags.add(tag)
        article.save()

        self.stdout.write('Done')