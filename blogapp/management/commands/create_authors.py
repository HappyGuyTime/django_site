from typing import Optional, Any

from django.core.management import BaseCommand

from blogapp.models import Author

class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        self.stdout.write('Create authors')
        authors_data = [
                    ('John', 'is real John'),
                    ('David', 'is real David'),
                    ('Joan', 'is real Joan'),
                ]
        authors = [
            Author(name=name, bio=bio)
            for name, bio in authors_data
        ]
        Author.objects.bulk_create(authors)

        self.stdout.write('Done')