# Generated by Django 3.1.4 on 2022-11-27 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlistitem',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]