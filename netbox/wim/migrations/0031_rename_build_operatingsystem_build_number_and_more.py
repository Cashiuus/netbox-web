# Generated by Django 4.1.9 on 2023-06-14 21:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('wim', '0030_operatingsystem_platform_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='operatingsystem',
            old_name='build',
            new_name='build_number',
        ),
        migrations.RemoveField(
            model_name='operatingsystem',
            name='family',
        ),
        migrations.AddField(
            model_name='operatingsystem',
            name='platform_family',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]