# Generated by Django 5.0.7 on 2024-09-21 06:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myquiz', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='academic_session',
        ),
    ]