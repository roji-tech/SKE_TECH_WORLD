# Generated by Django 5.0.7 on 2024-09-21 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_academicsession_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='term',
            name='is_current',
            field=models.BooleanField(default=False),
        ),
    ]
