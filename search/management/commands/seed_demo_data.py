from django.core.management.base import BaseCommand

from search.embedding import embed_text, get_model_name
from search.models import SearchDocument
from search.sample_data import DEMO_DOCUMENTS


class Command(BaseCommand):
    help = "Create or refresh the demo vector-search rows."

    def handle(self, *args, **options):
        model_name = get_model_name()

        for row in DEMO_DOCUMENTS:
            SearchDocument.objects.update_or_create(
                title=row["title"],
                defaults={
                    "category": row["category"],
                    "body": row["body"],
                    "embedding": embed_text(f"{row['title']} {row['body']}"),
                    "embedding_model": model_name,
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {len(DEMO_DOCUMENTS)} vector-search rows with {model_name}."
            )
        )
