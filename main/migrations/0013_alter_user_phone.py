# Generated by Django 5.0.7 on 2024-08-31 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(default='+234----', max_length=20),
        ),
    ]
