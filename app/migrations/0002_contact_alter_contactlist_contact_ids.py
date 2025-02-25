# Generated by Django 4.2.19 on 2025-02-25 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('contact_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('additional_personal_emails', models.TextField(blank=True, null=True)),
                ('business_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('business_email_last_seen', models.DateTimeField(blank=True, null=True)),
                ('business_email_validation_status', models.CharField(blank=True, max_length=255, null=True)),
                ('company_address', models.TextField(blank=True, null=True)),
                ('company_city', models.CharField(blank=True, max_length=255, null=True)),
                ('company_country_name', models.CharField(blank=True, max_length=255, null=True)),
                ('country_name', models.CharField(blank=True, max_length=255, null=True)),
                ('company_domain', models.CharField(blank=True, max_length=255, null=True)),
                ('company_founded_year', models.IntegerField(blank=True, null=True)),
                ('company_headline', models.TextField(blank=True, null=True)),
                ('company_identifier', models.CharField(blank=True, max_length=255, null=True)),
                ('company_linkedin_id', models.CharField(blank=True, max_length=255, null=True)),
                ('company_linkedin_url', models.URLField(blank=True, null=True)),
                ('company_locality', models.CharField(blank=True, max_length=255, null=True)),
                ('company_logo', models.URLField(blank=True, null=True)),
                ('company_name', models.CharField(blank=True, max_length=255, null=True)),
                ('company_phone', models.CharField(blank=True, max_length=255, null=True)),
                ('company_primary_industry', models.CharField(blank=True, max_length=255, null=True)),
                ('company_region1', models.CharField(blank=True, max_length=255, null=True)),
                ('company_size', models.CharField(blank=True, max_length=255, null=True)),
                ('company_slug', models.CharField(blank=True, max_length=255, null=True)),
                ('company_state', models.CharField(blank=True, max_length=255, null=True)),
                ('company_type', models.CharField(blank=True, max_length=255, null=True)),
                ('company_zip', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('direct_number', models.CharField(blank=True, max_length=255, null=True)),
                ('employee_count', models.IntegerField(blank=True, null=True)),
                ('employees_range', models.CharField(blank=True, max_length=255, null=True)),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('full_name', models.CharField(blank=True, max_length=255, null=True)),
                ('headline', models.TextField(blank=True, null=True)),
                ('industry_id', models.CharField(blank=True, max_length=255, null=True)),
                ('industry_name', models.CharField(blank=True, max_length=255, null=True)),
                ('interests', models.TextField(blank=True, null=True)),
                ('job_title', models.CharField(blank=True, max_length=255, null=True)),
                ('keywords', models.TextField(blank=True, null=True)),
                ('jobs_count', models.IntegerField(blank=True, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('linkedin_url', models.URLField(blank=True, null=True)),
                ('locality', models.CharField(blank=True, max_length=255, null=True)),
                ('mobile_phone', models.CharField(blank=True, max_length=255, null=True)),
                ('people_in_company', models.IntegerField(blank=True, null=True)),
                ('personal_phone', models.CharField(blank=True, max_length=255, null=True)),
                ('position_company_name', models.CharField(blank=True, max_length=255, null=True)),
                ('position_linkedin_company_id', models.CharField(blank=True, max_length=255, null=True)),
                ('position_locality', models.CharField(blank=True, max_length=255, null=True)),
                ('position_start_date', models.DateTimeField(blank=True, null=True)),
                ('position_start_date_month', models.IntegerField(blank=True, null=True)),
                ('position_start_date_year', models.IntegerField(blank=True, null=True)),
                ('position_summary', models.TextField(blank=True, null=True)),
                ('professional_address1', models.TextField(blank=True, null=True)),
                ('professional_city', models.CharField(blank=True, max_length=255, null=True)),
                ('professional_country', models.CharField(blank=True, max_length=255, null=True)),
                ('professional_state', models.CharField(blank=True, max_length=255, null=True)),
                ('professional_zip', models.CharField(blank=True, max_length=255, null=True)),
                ('profile_id', models.CharField(blank=True, max_length=255, null=True)),
                ('profile_picture', models.URLField(blank=True, null=True)),
                ('skills', models.TextField(blank=True, null=True)),
                ('slug', models.CharField(blank=True, max_length=255, null=True)),
                ('source', models.IntegerField(blank=True, null=True)),
                ('summary', models.TextField(blank=True, null=True)),
                ('technology_names', models.TextField(blank=True, null=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('verified_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('verified_email_at', models.DateTimeField(blank=True, null=True)),
                ('verified_email_quality', models.CharField(blank=True, max_length=255, null=True)),
                ('is_hiring', models.BooleanField(blank=True, null=True)),
                ('company_continent', models.CharField(blank=True, max_length=255, null=True)),
                ('personal_continent', models.CharField(blank=True, max_length=255, null=True)),
                ('personal_region1', models.CharField(blank=True, max_length=255, null=True)),
                ('personal_region2', models.CharField(blank=True, max_length=255, null=True)),
                ('has_phone', models.BooleanField(blank=True, null=True)),
                ('has_email', models.BooleanField(blank=True, null=True)),
                ('keywords_formatted', models.TextField(blank=True, null=True)),
                ('keywords_plan', models.TextField(blank=True, null=True)),
                ('description_plan', models.TextField(blank=True, null=True)),
                ('match_fields_list', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('email_history', models.TextField(blank=True, null=True)),
                ('suitability_rank', models.IntegerField(blank=True, null=True)),
                ('suitability_summary', models.TextField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AlterField(
            model_name='contactlist',
            name='contact_ids',
            field=models.JSONField(default=list, help_text='List of contact IDs from BigQuery'),
        ),
    ]
