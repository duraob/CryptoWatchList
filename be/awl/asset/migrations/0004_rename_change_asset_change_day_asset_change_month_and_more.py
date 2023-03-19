# Generated by Django 4.1.7 on 2023-03-18 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0003_remove_asset_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='asset',
            old_name='change',
            new_name='change_day',
        ),
        migrations.AddField(
            model_name='asset',
            name='change_month',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='asset',
            name='change_week',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
