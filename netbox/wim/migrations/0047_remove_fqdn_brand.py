# Generated by Django 4.1.9 on 2023-09-22 16:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('wim', '0046_alter_brand_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fqdn',
            name='brand',
        ),
    ]