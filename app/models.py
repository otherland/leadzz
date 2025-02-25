from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

# Create your models here.

class ContactList(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    contact_ids = models.JSONField(help_text="List of contact IDs from BigQuery", default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact List"
        verbose_name_plural = "Contact Lists"

    def __str__(self):
        return f"{self.title} ({self.contact_count} contacts)"

    @property
    def contact_count(self):
        return len(self.contact_ids or [])

class Contact(models.Model):
    contact_id = models.CharField(max_length=255, primary_key=True)
    additional_personal_emails = models.TextField(null=True, blank=True)
    business_email = models.EmailField(null=True, blank=True)
    business_email_last_seen = models.DateTimeField(null=True, blank=True)
    business_email_validation_status = models.CharField(max_length=255, null=True, blank=True)
    company_address = models.TextField(null=True, blank=True)
    company_city = models.CharField(max_length=255, null=True, blank=True)
    company_country_name = models.CharField(max_length=255, null=True, blank=True)
    country_name = models.CharField(max_length=255, null=True, blank=True)
    company_domain = models.CharField(max_length=255, null=True, blank=True)
    company_founded_year = models.IntegerField(null=True, blank=True)
    company_headline = models.TextField(null=True, blank=True)
    company_identifier = models.CharField(max_length=255, null=True, blank=True)
    company_linkedin_id = models.CharField(max_length=255, null=True, blank=True)
    company_linkedin_url = models.URLField(null=True, blank=True)
    company_locality = models.CharField(max_length=255, null=True, blank=True)
    company_logo = models.URLField(null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    company_phone = models.CharField(max_length=255, null=True, blank=True)
    company_primary_industry = models.CharField(max_length=255, null=True, blank=True)
    company_region1 = models.CharField(max_length=255, null=True, blank=True)
    company_size = models.CharField(max_length=255, null=True, blank=True)
    company_slug = models.CharField(max_length=255, null=True, blank=True)
    company_state = models.CharField(max_length=255, null=True, blank=True)
    company_type = models.CharField(max_length=255, null=True, blank=True)
    company_zip = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    direct_number = models.CharField(max_length=255, null=True, blank=True)
    employee_count = models.IntegerField(null=True, blank=True)
    employees_range = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    headline = models.TextField(null=True, blank=True)
    industry_id = models.CharField(max_length=255, null=True, blank=True)
    industry_name = models.CharField(max_length=255, null=True, blank=True)
    interests = models.TextField(null=True, blank=True)
    job_title = models.CharField(max_length=255, null=True, blank=True)
    keywords = models.TextField(null=True, blank=True)
    jobs_count = models.IntegerField(null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    locality = models.CharField(max_length=255, null=True, blank=True)
    mobile_phone = models.CharField(max_length=255, null=True, blank=True)
    people_in_company = models.IntegerField(null=True, blank=True)
    personal_phone = models.CharField(max_length=255, null=True, blank=True)
    position_company_name = models.CharField(max_length=255, null=True, blank=True)
    position_linkedin_company_id = models.CharField(max_length=255, null=True, blank=True)
    position_locality = models.CharField(max_length=255, null=True, blank=True)
    position_start_date = models.DateTimeField(null=True, blank=True)
    position_start_date_month = models.IntegerField(null=True, blank=True)
    position_start_date_year = models.IntegerField(null=True, blank=True)
    position_summary = models.TextField(null=True, blank=True)
    professional_address1 = models.TextField(null=True, blank=True)
    professional_city = models.CharField(max_length=255, null=True, blank=True)
    professional_country = models.CharField(max_length=255, null=True, blank=True)
    professional_state = models.CharField(max_length=255, null=True, blank=True)
    professional_zip = models.CharField(max_length=255, null=True, blank=True)
    profile_id = models.CharField(max_length=255, null=True, blank=True)
    profile_picture = models.URLField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    slug = models.CharField(max_length=255, null=True, blank=True)
    source = models.IntegerField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    technology_names = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    verified_email = models.EmailField(null=True, blank=True)
    verified_email_at = models.DateTimeField(null=True, blank=True)
    verified_email_quality = models.CharField(max_length=255, null=True, blank=True)
    is_hiring = models.BooleanField(null=True, blank=True)
    company_continent = models.CharField(max_length=255, null=True, blank=True)
    personal_continent = models.CharField(max_length=255, null=True, blank=True)
    personal_region1 = models.CharField(max_length=255, null=True, blank=True)
    personal_region2 = models.CharField(max_length=255, null=True, blank=True)
    has_phone = models.BooleanField(null=True, blank=True)
    has_email = models.BooleanField(null=True, blank=True)
    keywords_formatted = models.TextField(null=True, blank=True)
    keywords_plan = models.TextField(null=True, blank=True)
    description_plan = models.TextField(null=True, blank=True)
    match_fields_list = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    email_history = models.TextField(null=True, blank=True)
    suitability_rank = models.IntegerField(null=True, blank=True)
    suitability_summary = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        return f"{self.full_name} ({self.contact_id})"