# Generated by Django 5.1 on 2024-09-04 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='number',
            field=models.CharField(blank=True, max_length=10, unique=True, verbose_name='order number'),
        ),
    ]
