# Generated by Django 5.0.7 on 2024-09-05 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='librarybook',
            name='library',
        ),
        migrations.AddField(
            model_name='librarybook',
            name='book_image_url',
            field=models.URLField(default=1),
            preserve_default=False,
        ),
    ]
