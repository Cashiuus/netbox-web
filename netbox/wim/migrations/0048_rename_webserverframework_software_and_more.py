# Generated by Django 4.1.9 on 2023-09-23 20:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('extras', '0092_delete_jobresult'),
        ('wim', '0047_remove_fqdn_brand'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='WebserverFramework',
            new_name='Software',
        ),
        migrations.RemoveField(
            model_name='webemail',
            name='domain_tmp',
        ),
        migrations.AddField(
            model_name='webemail',
            name='domain',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='emails',
                to='wim.domain',
            ),
        ),
        migrations.AlterField(
            model_name='webemail',
            name='email_address',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]