# Generated by Django 5.0.7 on 2024-09-08 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_remove_librarybook_isbn_librarybook_uploaded_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='librarybook',
            name='book',
            field=models.FileField(default=1, upload_to='library/'),
            preserve_default=False,
        ),
    ]
