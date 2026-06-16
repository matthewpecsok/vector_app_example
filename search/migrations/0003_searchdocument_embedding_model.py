from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("search", "0002_seed_demo_documents"),
    ]

    operations = [
        migrations.AddField(
            model_name="searchdocument",
            name="embedding_model",
            field=models.CharField(blank=True, default="", max_length=160),
        ),
    ]
