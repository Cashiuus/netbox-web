# Generated by Django 4.1.9 on 2023-06-03 00:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('wim', '0004_remove_fqdn_geo_region_orig_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitelocation',
            name='code',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]