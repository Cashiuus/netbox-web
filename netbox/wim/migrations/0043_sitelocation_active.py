# Generated by Django 4.1.9 on 2023-08-29 01:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('wim', '0042_fqdn_is_nonprod_mirror'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitelocation',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
