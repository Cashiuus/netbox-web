# Generated by Django 4.1.9 on 2023-12-11 20:21

from django.db import migrations, models
import taggit.managers
import utilities.json


class Migration(migrations.Migration):
    dependencies = [
        ('extras', '0092_delete_jobresult'),
        ('wim', '0052_alter_operatingsystem_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                (
                    'custom_field_data',
                    models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder),
                ),
                ('description', models.CharField(blank=True, max_length=255)),
                ('comments', models.TextField(blank=True)),
                ('hash_sha1', models.CharField(max_length=50, unique=True)),
                ('hash_sha256', models.CharField(blank=True, max_length=65)),
                ('hash_md5', models.CharField(blank=True, max_length=30)),
                ('sdn', models.CharField(max_length=400)),
                ('scn', models.CharField(max_length=400)),
                ('san', models.TextField()),
                ('sorg', models.CharField(blank=True, max_length=400)),
                ('idn', models.CharField(max_length=400)),
                ('icn', models.CharField(max_length=400)),
                ('iorg', models.CharField(max_length=400)),
                ('date_issued', models.DateField(blank=True)),
                ('date_expiration', models.DateField()),
                ('signing_algorithm', models.CharField(blank=True, max_length=20)),
                ('key_type', models.CharField(blank=True, max_length=20)),
                ('key_bitlength', models.CharField(blank=True, max_length=20)),
                ('is_wildcard', models.BooleanField(default=False)),
                ('is_self_signed', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'verbose_name': 'Certificate',
                'verbose_name_plural': 'Certificates',
                'ordering': ['scn'],
            },
        ),
    ]