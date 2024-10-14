# Generated by Django 5.0.7 on 2024-09-28 14:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myquiz', '0004_alter_question_image_alter_questionbank_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='exclude',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='question',
            name='option_1',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='question',
            name='option_2',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='question',
            name='option_3',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='question',
            name='option_4',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='created_by',
            field=models.ForeignKey(limit_choices_to={'role__in': ['teacher']}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]