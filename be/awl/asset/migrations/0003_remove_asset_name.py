# Generated by Django 4.1.7 on 2023-03-18 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0002_rename_dividend_asset_change_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asset',
            name='name',
        ),
    ]
