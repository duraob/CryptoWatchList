# Generated by Django 4.1.7 on 2023-03-12 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=10)),
                ('quote', models.FloatField()),
                ('pe', models.FloatField()),
                ('dividend', models.FloatField()),
                ('ma50', models.FloatField()),
                ('ma200', models.FloatField()),
            ],
        ),
    ]