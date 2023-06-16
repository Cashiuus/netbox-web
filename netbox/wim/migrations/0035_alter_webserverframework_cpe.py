# Generated by Django 4.1.9 on 2023-06-15 19:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('wim', '0034_fqdn_compliance_programs_choice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webserverframework',
            name='cpe',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='webserver_frameworks',
                to='wim.cpe',
            ),
        ),
    ]
