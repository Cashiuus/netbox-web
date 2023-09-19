# Generated by Django 4.1.9 on 2023-09-07 15:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('wim', '0043_sitelocation_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fqdn',
            name='website_title',
            field=models.CharField(blank=True, default='', max_length=250),
        ),
        migrations.AlterField(
            model_name='fqdn',
            name='website_url',
            field=models.URLField(blank=True, max_length=900, null=True),
        ),
    ]
