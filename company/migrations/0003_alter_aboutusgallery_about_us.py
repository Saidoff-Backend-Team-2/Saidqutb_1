# Generated by Django 5.1 on 2024-08-22 12:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_rename_vidio_aboutus_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutusgallery',
            name='about_us',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='galleries', to='company.aboutus'),
        ),
    ]
