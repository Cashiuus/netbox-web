# Generated by Django 4.1.9 on 2023-09-22 15:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('wim', '0045_brand_domain_brand_fqdn_brand'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
    ]