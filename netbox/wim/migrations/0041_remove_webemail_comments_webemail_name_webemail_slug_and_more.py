# Generated by Django 4.1.9 on 2023-07-25 21:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('wim', '0040_rename_vuln_scan_last_date_fqdn_date_last_vulnscan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='webemail',
            name='comments',
        ),
        migrations.AddField(
            model_name='webemail',
            name='name',
            field=models.CharField(default='', max_length=100, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='webemail',
            name='slug',
            field=models.SlugField(default='', max_length=100, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='webemail',
            name='description',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]