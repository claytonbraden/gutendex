# Generated by Django 5.1.6 on 2025-02-27 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_format_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='format',
            name='name',
        ),
        migrations.AddField(
            model_name='book',
            name='gutenberg_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
