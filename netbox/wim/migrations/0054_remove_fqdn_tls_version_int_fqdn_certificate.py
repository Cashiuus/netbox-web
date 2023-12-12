# Generated by Django 4.1.9 on 2023-12-11 22:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('wim', '0053_certificate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fqdn',
            name='tls_version_int',
        ),
        migrations.AddField(
            model_name='fqdn',
            name='certificate',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='+',
                to='wim.certificate',
            ),
        ),
    ]
