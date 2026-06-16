from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SearchDocument",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=120)),
                ("category", models.CharField(max_length=40)),
                ("body", models.TextField()),
                ("embedding", models.JSONField()),
            ],
            options={
                "ordering": ["title"],
            },
        ),
    ]
