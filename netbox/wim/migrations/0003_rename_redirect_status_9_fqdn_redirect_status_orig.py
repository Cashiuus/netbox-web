# Generated by Django 4.1.9 on 2023-06-02 21:28

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('wim', '0002_rename_principal_location_businessdivision_principal_location_orig_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fqdn',
            old_name='redirect_status_9',
            new_name='redirect_status_orig',
        ),
    ]
