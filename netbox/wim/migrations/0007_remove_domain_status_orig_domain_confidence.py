# Generated by Django 4.1.9 on 2023-06-05 19:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('wim', '0006_rename_confidence_domain_confidence_orig'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='domain',
            name='status_orig',
        ),
        migrations.AddField(
            model_name='domain',
            name='confidence',
            field=models.CharField(default='CANDIDATE', max_length=50),
        ),
    ]
