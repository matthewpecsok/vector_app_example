from django.db import migrations


DEMO_DOCUMENTS = [
    {
        "title": "Rainy Day Forecast",
        "category": "Weather",
        "body": "Rain and cooler air are expected through the afternoon forecast.",
    },
    {
        "title": "Fresh Tomato Pasta",
        "category": "Food",
        "body": "A quick dinner with tomatoes, basil, garlic, olive oil, and parmesan.",
    },
    {
        "title": "Morning Trail Run",
        "category": "Health",
        "body": "A cardio workout with trail shoes, steady training pace, and heart rate notes.",
    },
    {
        "title": "Django Vector Search",
        "category": "Programming",
        "body": "Build a Python Django web app with database rows, vector embeddings, cosine similarity, and ranking scores.",
    },
    {
        "title": "Weekend in Lisbon",
        "category": "Travel",
        "body": "A travel plan with train routes, hotel choices, walking streets, and sunny plazas.",
    },
    {
        "title": "Budgeting for a Trip",
        "category": "Finance",
        "body": "Track travel expenses, hotel cash, daily budget, and money left for the return train.",
    },
    {
        "title": "NBA Playoff Recap",
        "category": "Sports",
        "body": "Basketball playoff notes with score swings, training intensity, and late-game defense.",
    },
    {
        "title": "Acoustic Guitar Practice",
        "category": "Music",
        "body": "Guitar practice with chords, melody changes, quiet timing, and warm music notes.",
    },
]


def seed_documents(apps, schema_editor):
    search_document = apps.get_model("search", "SearchDocument")
    for row in DEMO_DOCUMENTS:
        search_document.objects.update_or_create(
            title=row["title"],
            defaults={
                "category": row["category"],
                "body": row["body"],
                "embedding": [],
            },
        )


def remove_documents(apps, schema_editor):
    search_document = apps.get_model("search", "SearchDocument")
    titles = [row["title"] for row in DEMO_DOCUMENTS]
    search_document.objects.filter(title__in=titles).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("search", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_documents, remove_documents),
    ]
