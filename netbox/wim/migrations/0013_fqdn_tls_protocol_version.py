# Generated by Django 4.1.9 on 2023-06-06 16:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('wim', '0012_rename_tls_version_fqdn_tls_version_int'),
    ]

    operations = [
        migrations.AddField(
            model_name='fqdn',
            name='tls_protocol_version',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]