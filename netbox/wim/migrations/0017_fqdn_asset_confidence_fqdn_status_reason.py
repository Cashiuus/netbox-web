# Generated by Django 4.1.9 on 2023-06-06 23:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('wim', '0016_fqdn_private_ip_2_alter_domain_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fqdn',
            name='asset_confidence',
            field=models.CharField(default='Candidate', max_length=50),
        ),
        migrations.AddField(
            model_name='fqdn',
            name='status_reason',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
