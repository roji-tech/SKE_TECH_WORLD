# Generated by Django 5.0.7 on 2024-09-29 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myquiz', '0006_alter_result_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentanswer',
            name='selected_option',
            field=models.CharField(default='', max_length=200),
        ),
    ]
