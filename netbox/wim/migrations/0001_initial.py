import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import timezone_field.fields
import utilities.fields
import utilities.json


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('dcim', '0172_larger_power_draw_values'),
        ('tenancy', '0010_tenant_relax_uniqueness'),
        ('extras', '0092_delete_jobresult'),
        ('ipam', '0066_iprange_mark_utilized'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessCriticality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                (
                    'custom_field_data',
                    models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder),
                ),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.CharField(max_length=150)),
                ('order', models.SmallIntegerField(default=10)),
                ('color', utilities.fields.ColorField(default='9e9e9e', max_length=6)),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'verbose_name': 'Business Criticality',
                'verbose_name_plural': 'Business Criticalities',
                'ordering': ('order', 'name'),
            },
        ),
        migrations.CreateModel(
            name='BusinessDivision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                (
                    'custom_field_data',
                    models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder),
                ),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('acronym', models.CharField(max_length=10)),
                ('description', models.TextField(blank=True, default='')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Business Division',
                'verbose_name_plural': 'Business Divisions',
                'ordering': ['acronym'],
            },
        ),
        migrations.CreateModel(
            name='BusinessGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                (
                    'custom_field_data',
                    models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder),
                ),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('acronym', models.CharField(max_length=10)),
                ('description', models.TextField(blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                (
                    'principal_location_8',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='+',
                        to='dcim.site',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Business Group',
                'verbose_name_plural': 'Business Groups',
                'ordering': ['acronym'],
            },
        ),
        migrations.CreateModel(
            name='CloudProvider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                (
                    'custom_field_data',
                    models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder),
                ),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=75, unique=True)),
                ('description', models.TextField(blank=True)),
                ('testing_reqs', models.TextField(blank=True)),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ComplianceProgram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                (
                    'custom_field_data',
                    models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder),
                ),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('acronym', models.CharField(max_length=15, unique=True)),
                ('description', models.TextField()),
                ('website', models.URLField(blank=True, null=True)),
                ('mandates_pentesting_9', models.BooleanField(default=False, null=True)),
                ('mandates_vulnscanning_9', models.BooleanField(default=True, null=True)),
                ('order', models.SmallIntegerField(default=10)),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'verbose_name': 'compliance program',
                'verbose_name_plural': 'compliance programs',
                'ordering': ('acronym',),
            },
        ),
        migrations.CreateModel(
            name='CPE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('cpe', models.CharField(max_length=300, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'ordering': ('cpe',),
            },
        ),
        migrations.CreateModel(
            name='Domain',
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
                (
                    'name',
                    models.CharField(
                        max_length=255,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                code='invalid',
                                message='Only alphanumeric characters, asterisks, hyphens, periods, and underscores are allowed in DNS names',
                                regex='^([0-9A-Za-z_-]+|\\*)(\\.[0-9A-Za-z_-]+)*\\.?$',
                            )
                        ],
                    ),
                ),
                ('status_9', models.IntegerField(default=4)),
                ('status', models.CharField(default='new', max_length=50)),
                ('slug', models.SlugField(max_length=100)),
                ('date_registrar_expiry', models.DateField(blank=True, null=True)),
                ('date_first_registered', models.DateField(blank=True, null=True)),
                ('date_last_recon_scanned', models.DateField(blank=True, null=True)),
                ('is_internet_facing', models.BooleanField(default=True, null=True)),
                ('is_flagship', models.BooleanField(default=False, null=True)),
                ('confidence', models.IntegerField(default=2)),
                ('meets_standards', models.BooleanField(default=True, null=True)),
                ('registrar_iana_id_9', models.IntegerField(blank=True, null=True)),
                ('registrar_company_9', models.CharField(blank=True, max_length=255)),
                ('registrant_org', models.CharField(blank=True, max_length=255)),
                ('registration_emails_9', models.TextField(blank=True)),
                ('registrar_domain_statuses', models.TextField(blank=True, default='')),
                ('nameservers', models.TextField(blank=True)),
                ('mail_servers', models.CharField(blank=True, default='', max_length=255)),
                ('whois_servers', models.CharField(blank=True, default='', max_length=255)),
                ('soa_nameservers', models.CharField(blank=True, default='', max_length=255)),
                ('soa_email', models.EmailField(blank=True, default='', max_length=255)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True, default='')),
            ],
            options={
                'verbose_name': 'Domain',
                'verbose_name_plural': 'Domains',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='WebsiteStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                (
                    'custom_field_data',
                    models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder),
                ),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField()),
                ('order', models.SmallIntegerField(default=10)),
                ('color', utilities.fields.ColorField(default='9e9e9e', max_length=6)),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'verbose_name': 'Website Status',
                'verbose_name_plural': 'Website Statuses',
                'ordering': ('order', 'name'),
            },
        ),
        migrations.CreateModel(
            name='WebsiteAuthType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                (
                    'custom_field_data',
                    models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder),
                ),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('order', models.SmallIntegerField(default=10)),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'verbose_name': 'Auth Type',
                'verbose_name_plural': 'Auth Types',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='WebserverFramework',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                (
                    'custom_field_data',
                    models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder),
                ),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('product', models.CharField(blank=True, default='', max_length=250)),
                ('version', models.CharField(blank=True, default='', max_length=50)),
                ('order', models.SmallIntegerField(default=10)),
                ('notes', models.TextField(blank=True)),
                (
                    'cpe',
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='webserver_frameworks',
                        to='wim.cpe',
                    ),
                ),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'verbose_name': 'Webserver Framework',
                'verbose_name_plural': 'Webserver Frameworks',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='WebEmail',
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
                ('email_address', models.EmailField(blank=True, max_length=254, unique=True)),
                ('domain_tmp', models.CharField(max_length=150)),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'ordering': ('email_address',),
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                (
                    'custom_field_data',
                    models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder),
                ),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SupportGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                (
                    'custom_field_data',
                    models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder),
                ),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True)),
                ('group_type', models.IntegerField(default=1)),
                ('group_members', models.TextField(blank=True, default='')),
                ('group_leader', models.CharField(blank=True, default='', max_length=255)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('division', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wim.businessdivision')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wim.businessgroup')),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'verbose_name': 'Support Group',
                'verbose_name_plural': 'Support Groups',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='SiteLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                (
                    'custom_field_data',
                    models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder),
                ),
                ('description', models.CharField(blank=True, max_length=200)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('priority', models.PositiveSmallIntegerField(default=50)),
                ('street', models.CharField(blank=True, default='', max_length=255)),
                ('city', models.CharField(blank=True, default='', max_length=50)),
                ('state', models.CharField(blank=True, default='', max_length=50)),
                ('country_1', models.CharField(default='US', max_length=5)),
                ('geo_region_9', models.IntegerField(default=1)),
                ('timezone_1', models.CharField(blank=True, default='', max_length=50)),
                ('timezone', timezone_field.fields.TimeZoneField(blank=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=8, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('it_infra_contact', models.CharField(blank=True, default='', max_length=255)),
                ('approx_network_size', models.IntegerField(blank=True, null=True)),
                ('ranges_tmp1', models.TextField(blank=True, default='')),
                ('notes', models.TextField(blank=True, default='')),
                ('asns', models.ManyToManyField(blank=True, related_name='sitelocations', to='ipam.asn')),
                (
                    'geo_region',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='sitelocations',
                        to='dcim.region',
                    ),
                ),
                (
                    'impacted_division',
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wim.businessdivision'
                    ),
                ),
                (
                    'impacted_group',
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wim.businessgroup'
                    ),
                ),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
                (
                    'tenant',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='sitelocations',
                        to='tenancy.tenant',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Site Location',
                'verbose_name_plural': 'Site Locations',
                'ordering': ('code',),
            },
        ),
        migrations.CreateModel(
            name='Registrar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                (
                    'custom_field_data',
                    models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder),
                ),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('iana_id', models.IntegerField(blank=True, null=True)),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ParkedStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                (
                    'custom_field_data',
                    models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder),
                ),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField()),
                ('order', models.SmallIntegerField(default=10)),
                ('color', utilities.fields.ColorField(default='9e9e9e', max_length=6)),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'verbose_name': 'Parked Status',
                'verbose_name_plural': 'Parked Statuses',
                'ordering': ('order', 'name'),
            },
        ),
        migrations.CreateModel(
            name='OperatingSystem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                (
                    'custom_field_data',
                    models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder),
                ),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('vendor', models.CharField(max_length=100)),
                ('product', models.CharField(max_length=100)),
                ('family', models.CharField(blank=True, max_length=100)),
                ('update', models.CharField(blank=True, max_length=10)),
                ('build', models.CharField(blank=True, max_length=50)),
                ('color', utilities.fields.ColorField(default='9e9e9e', max_length=6)),
                (
                    'cpe',
                    models.OneToOneField(
                        blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='wim.cpe'
                    ),
                ),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'verbose_name': 'operating system',
                'verbose_name_plural': 'operating systems',
                'ordering': ['vendor', 'product'],
                'unique_together': {('vendor', 'product', 'update')},
            },
        ),
        migrations.CreateModel(
            name='FqdnStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                (
                    'custom_field_data',
                    models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder),
                ),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField()),
                ('order', models.SmallIntegerField(default=10)),
                ('color', utilities.fields.ColorField(default='9e9e9e', max_length=6)),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'verbose_name': 'FQDN Status',
                'verbose_name_plural': 'FQDN Statuses',
                'ordering': ('order', 'name'),
            },
        ),
        migrations.CreateModel(
            name='FQDN',
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
                (
                    'name',
                    models.CharField(
                        max_length=255,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                code='invalid',
                                message='Only alphanumeric characters, asterisks, hyphens, periods, and underscores are allowed in DNS names',
                                regex='^([0-9A-Za-z_-]+|\\*)(\\.[0-9A-Za-z_-]+)*\\.?$',
                            )
                        ],
                    ),
                ),
                ('slug', models.SlugField(max_length=100)),
                ('status_9', models.IntegerField(default=4)),
                ('status', models.CharField(default='new', max_length=50)),
                ('asset_class', models.CharField(default='fqdn', max_length=50)),
                ('role', models.CharField(blank=True, max_length=50)),
                ('public_ip_9', models.GenericIPAddressField(blank=True, null=True, protocol='IPv4')),
                ('private_ip_9', models.GenericIPAddressField(blank=True, null=True, protocol='IPv4')),
                ('hostname_9', models.CharField(blank=True, default='', max_length=100)),
                ('os_9', models.CharField(blank=True, default='', max_length=100)),
                ('owners_9', models.TextField(blank=True)),
                ('is_in_cmdb', models.BooleanField(default=False, null=True)),
                ('geo_region_9', models.IntegerField(default=1)),
                ('criticality_score_1', models.PositiveSmallIntegerField(default=50)),
                ('env_used_for_1', models.IntegerField(default=3)),
                ('architectural_model_1', models.IntegerField(default=1)),
                ('tech_addtl', models.TextField(blank=True, default='')),
                ('cnames', models.CharField(blank=True, default='', max_length=500)),
                ('dns_a_record_ips', models.TextField(blank=True, default='')),
                ('tls_cert_info', models.TextField(blank=True, default='')),
                ('tls_cert_expires', models.DateField(blank=True, null=True)),
                ('tls_cert_sha1', models.CharField(blank=True, default='', max_length=50)),
                ('tls_cert_is_wildcard', models.BooleanField(default=None, null=True)),
                ('tls_version', models.IntegerField(blank=True, default=None, null=True)),
                ('is_vhost', models.BooleanField(default=False, null=True)),
                ('is_http2', models.BooleanField(default=False, null=True)),
                ('response_code', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('content_length', models.PositiveIntegerField(blank=True, null=True)),
                ('redirect_status_9', models.IntegerField(blank=True, null=True)),
                ('redirect_health', models.CharField(blank=True, max_length=50)),
                ('redirect_url', models.URLField(blank=True, max_length=400, null=True)),
                ('is_internet_facing', models.BooleanField(default=True, null=True)),
                ('is_flagship', models.BooleanField(default=False, null=True)),
                ('is_cloud_hosted', models.BooleanField(default=True, null=True)),
                ('is_vendor_managed', models.BooleanField(default=False, null=True)),
                ('is_vendor_hosted', models.BooleanField(default=False, null=True)),
                ('is_akamai', models.BooleanField(default=False, null=True)),
                ('is_load_protected', models.BooleanField(default=False, null=True)),
                ('is_waf_protected', models.BooleanField(default=False, null=True)),
                ('vendor_pocs_9', models.CharField(blank=True, default='', max_length=500)),
                ('vendor_url', models.URLField(blank=True, null=True)),
                ('vendor_notes', models.TextField(blank=True, default='')),
                ('website_url', models.URLField(blank=True, max_length=400, null=True)),
                ('website_title', models.CharField(blank=True, default='', max_length=150)),
                ('website_email', models.EmailField(blank=True, default='', max_length=254)),
                ('website_homepage_image', models.ImageField(blank=True, upload_to='wim-images')),
                ('had_bugbounty', models.BooleanField(default=False, null=True)),
                ('is_risky', models.BooleanField(default=False, null=True)),
                ('site_operation_age', models.DateField(default=datetime.date.today)),
                ('last_vuln_assessment', models.DateField(blank=True, null=True)),
                ('vuln_assessment_priority', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('vuln_scan_coverage', models.BooleanField(default=False, null=True)),
                ('vuln_scan_last_date', models.DateField(blank=True, null=True)),
                ('risk_analysis_notes', models.TextField(blank=True, default='')),
                ('feature_acct_mgmt', models.BooleanField(default=False, null=True)),
                ('feature_auth_self_registration', models.BooleanField(default=False, null=True)),
                ('feature_api', models.BooleanField(default=False, null=True)),
                ('scoping_size', models.PositiveSmallIntegerField(default=1)),
                ('scoping_complexity', models.PositiveSmallIntegerField(default=1)),
                ('scoping_roles', models.PositiveSmallIntegerField(default=0)),
                ('is_compliance_required', models.BooleanField(default=False, null=True)),
                ('notes', models.TextField(blank=True, default='')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                (
                    'cloud_provider_9',
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='wim.cloudprovider'
                    ),
                ),
                (
                    'compliance_programs',
                    models.ManyToManyField(blank=True, default='', related_name='fqdns', to='wim.complianceprogram'),
                ),
                (
                    'domain',
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wim.domain'
                    ),
                ),
                (
                    'feature_auth_type',
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wim.websiteauthtype'
                    ),
                ),
                (
                    'fqdn_status',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='fqdns',
                        to='wim.fqdnstatus',
                    ),
                ),
                (
                    'geo_region',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='fqdns',
                        to='dcim.region',
                    ),
                ),
                (
                    'impacted_division_9',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='fqdns',
                        to='wim.businessdivision',
                    ),
                ),
                (
                    'impacted_group_9',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='fqdns',
                        to='wim.businessgroup',
                    ),
                ),
                (
                    'ipaddress_private_8',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='fqdns_private',
                        to='ipam.ipaddress',
                    ),
                ),
                (
                    'ipaddress_public_8',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='fqdns_public',
                        to='ipam.ipaddress',
                    ),
                ),
                (
                    'location',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='fqdns',
                        to='dcim.site',
                    ),
                ),
                (
                    'location_9',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='fqdns',
                        to='wim.sitelocation',
                    ),
                ),
                (
                    'os_1',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='+',
                        to='wim.operatingsystem',
                    ),
                ),
                (
                    'os_8',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='+',
                        to='dcim.platform',
                    ),
                ),
                (
                    'parked_status',
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='wim.parkedstatus'
                    ),
                ),
                (
                    'snow_bcdr_criticality',
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='wim.businesscriticality'
                    ),
                ),
                (
                    'support_group_website_approvals',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='fqdns_business',
                        to='wim.supportgroup',
                    ),
                ),
                (
                    'support_group_website_technical',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='fqdns_technical',
                        to='wim.supportgroup',
                    ),
                ),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
                (
                    'tech_webserver_1',
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wim.webserverframework'
                    ),
                ),
                (
                    'tenant',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='fqdns',
                        to='tenancy.tenant',
                    ),
                ),
                (
                    'vendor_company_1',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, related_name='fqdns', to='wim.vendor'
                    ),
                ),
                (
                    'website_status',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='fqdns',
                        to='wim.websitestatus',
                    ),
                ),
            ],
            options={
                'verbose_name': 'FQDN',
                'verbose_name_plural': 'FQDNs',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='domain',
            name='registrar_company',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='domains',
                to='wim.registrar',
            ),
        ),
        migrations.AddField(
            model_name='domain',
            name='registration_emails',
            field=models.ManyToManyField(blank=True, related_name='domains', to='wim.webemail'),
        ),
        migrations.AddField(
            model_name='domain',
            name='tags',
            field=taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag'),
        ),
        migrations.AddField(
            model_name='domain',
            name='tenant',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='domains',
                to='tenancy.tenant',
            ),
        ),
        migrations.AddField(
            model_name='businessgroup',
            name='principal_location_9',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='+',
                to='wim.sitelocation',
            ),
        ),
        migrations.AddField(
            model_name='businessgroup',
            name='tags',
            field=taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag'),
        ),
        migrations.AddField(
            model_name='businessdivision',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wim.businessgroup'),
        ),
        migrations.AddField(
            model_name='businessdivision',
            name='principal_location',
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wim.sitelocation'
            ),
        ),
        migrations.AddField(
            model_name='businessdivision',
            name='tags',
            field=taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag'),
        ),
    ]
