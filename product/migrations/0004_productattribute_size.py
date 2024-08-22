# Generated by Django 5.1 on 2024-08-22 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_product_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='productattribute',
            name='size',
            field=models.CharField(default=1, help_text='in liters', verbose_name='size'),
            preserve_default=False,
        ),
    ]
