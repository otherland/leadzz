# Generated by Django 4.2.19 on 2025-02-25 12:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BigQueryContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('company_name', models.CharField(max_length=255)),
                ('job_title', models.CharField(max_length=255)),
                ('industry_name', models.CharField(max_length=255)),
                ('company_country_name', models.CharField(max_length=255)),
                ('employees_range', models.CharField(max_length=255)),
                ('company_domain', models.TextField()),
                ('linkedin_url', models.TextField()),
                ('company_linkedin_url', models.TextField()),
                ('company_logo', models.TextField()),
                ('description', models.TextField()),
            ],
            options={
                'db_table': None,
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ContactList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('contact_ids', models.JSONField(help_text='List of contact IDs from BigQuery')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Contact List',
                'verbose_name_plural': 'Contact Lists',
                'ordering': ['-created_at'],
            },
        ),
    ]
