# Generated by Django 5.0.7 on 2024-09-29 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myquiz', '0005_question_exclude_alter_question_option_1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='score',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=5),
        ),
    ]
