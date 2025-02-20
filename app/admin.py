from django.utils.html import format_html
from django.contrib import admin
from .bigquery import fetch_contacts, get_unique_values
from django.db import models
import logging
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.db.models.sql import Query
import random

from django.core.cache import cache
from unfold.admin import ModelAdmin  # Change this import
from unfold.contrib.filters.admin import DropdownFilter, MultipleDropdownFilter
from django.utils.translation import gettext_lazy as _

EMPTY_VALUES = (None, '')

logger = logging.getLogger(__name__)

class BaseFilter(MultipleDropdownFilter):
    def queryset(self, request, queryset):
        # Get all active filters at once
        active_filters = {}
        for key in ['industry_name', 'company_country_name', 'employees_range']:
            if key in request.GET:
                active_filters[key] = request.GET.getlist(key)[0]  # Get first value if list
        
        if active_filters:
            return fetch_contacts(filters=active_filters)
        return queryset

class BaseMultipleFilter(MultipleDropdownFilter):
    def value(self):
        values = super().value()
        if values:
            # If it's already a list, return it
            if isinstance(values, (list, tuple)):
                return values
            # If it's a string, split by comma
            if isinstance(values, str):
                return values.split(',')
        return None

    def queryset(self, request, queryset):
        # Pass-through method - actual filtering is handled in admin's get_queryset
        return queryset

class IndustryFilter(BaseMultipleFilter):
    title = _('Industry')
    parameter_name = 'industry_name'

    def lookups(self, request, model_admin):
        cache_key = f'filter_lookups_industry'
        cached_values = cache.get(cache_key)
        if cached_values is None:
            values = get_unique_values('industry_name', limit=1000)
            cached_values = [(value, value.title()) for value in values]
            cache.set(cache_key, cached_values, 3600)
        return cached_values

class JobTitleFilter(DropdownFilter):
    title = _('Job Title')
    parameter_name = 'job_title'

    def lookups(self, request, model_admin):
        cache_key = f'filter_lookups_job_title'
        cached_values = cache.get(cache_key)
        if cached_values is None:
            values = get_unique_values('job_title', limit=2500)
            cached_values = [(value, value) for value in values]
            cache.set(cache_key, cached_values, 3600)
        return cached_values

    def queryset(self, request, queryset):
        if self.value() not in EMPTY_VALUES:
            return fetch_contacts(filters={'job_title': self.value()})
        return queryset

class CountryFilter(BaseMultipleFilter):
    title = _('Country')
    parameter_name = 'company_country_name'

    def lookups(self, request, model_admin):
        cache_key = f'filter_lookups_country'
        cached_values = cache.get(cache_key)
        if cached_values is None:
            values = get_unique_values('company_country_name', limit=1000)
            cached_values = [(value, value.title()) for value in values]
            cache.set(cache_key, cached_values, 3600)
        return cached_values

class EmployeesRangeFilter(BaseMultipleFilter):
    title = _('Employees Range')
    parameter_name = 'employees_range'

    def lookups(self, request, model_admin):
        cache_key = f'filter_lookups_employees_range'
        cached_values = cache.get(cache_key)
        if cached_values is None:
            values = get_unique_values('employees_range', limit=1000)
            cached_values = [(value, value.title()) for value in values]
            cache.set(cache_key, cached_values, 3600)
        return cached_values

class BigQueryContact(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    full_name = models.CharField(max_length=255)
    business_email = models.TextField()
    additional_personal_emails = models.TextField()
    company_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    industry_name = models.CharField(max_length=255)
    company_country_name = models.CharField(max_length=255)
    company_size = models.CharField(max_length=255)
    employees_range = models.CharField(max_length=255)
    mobile_phone = models.CharField(max_length=255)
    personal_phone = models.CharField(max_length=255)
    company_phone = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    company_domain = models.TextField()
    company_linkedin_url = models.TextField()
    linkedin_url = models.TextField()
    company_logo = models.TextField()
    description = models.TextField()

    class Meta:
        managed = False
        app_label = 'app'
        db_table = None  # Important: this tells Django there's no actual table
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __str__(self):
        return f"{self.full_name}"

    @classmethod
    def from_db(cls, db, field_names, values):
        # This is needed to handle the BigQuery results
        if isinstance(values, dict):
            instance = cls(**values)
        else:
            instance = super().from_db(db, field_names, values)
        return instance

    def _get_pk_val(self, meta=None):
        return self.id

class BigQueryQuerySet(QuerySet):
    def __init__(self, instances=None, model=None):
        self.model = model or BigQueryContact
        self._result_cache = instances or []
        self._db = None
        self._hints = {}
        self._prefetch_related_lookups = []
        self._sticky_filter = False
        self._query = Query(self.model)
        
    @property
    def query(self):
        return self._query
        
    @query.setter
    def query(self, value):
        self._query = value or Query(self.model)
        
    def count(self):
        return len(self._result_cache)
        
    def __len__(self):
        return len(self._result_cache)
        
    def __iter__(self):
        return iter(self._result_cache)
        
    def __getitem__(self, k):
        print(f"DEBUG: Getting item {k}")
        if isinstance(k, slice):
            return self._result_cache[0:50]  # Always return first 50 items
        return self._result_cache[k]
        
    def all(self):
        return self
        
    def filter(self, *args, **kwargs):
        return self
        
    def order_by(self, *args, **kwargs):
        return self

class BigQueryContactAdmin(ModelAdmin):
    list_display = (
        'full_name_display',
        'company_logo_display',
        'company_name_display',
        'job_title_display',
        'business_email_display',
        'mobile_phone_display',
        'personal_phone_display',
        'additional_personal_emails_display',
        'industry_name_display',
        'company_linkedin_url_display',
        'company_domain_display',
        'linkedin_url_display',
        'company_phone_display',
        'company_country_name_display',
        'employees_range',
        'description_display',
    )


    # For model fields, use custom labels
    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        self.model._meta.get_field('job_title').verbose_name = 'Job Title'
        self.model._meta.get_field('industry_name').verbose_name = 'Industry'
        self.model._meta.get_field('company_name').verbose_description = 'Company'
        self.model._meta.get_field('company_domain').verbose_name = 'URL'
        self.model._meta.get_field('company_country_name').verbose_name = 'Country'
        self.model._meta.get_field('employees_range').verbose_name = 'Company Size'
        return list_display

    def truncate_text(self, text, length=30):
        """Helper method to truncate text and add ellipsis"""
        if not text:
            return "-"
        text = str(text)  # Convert to string in case it's not
        if len(text) <= length:
            return text
        return format_html(
            '<span title="{}">{}&hellip;</span>',
            text,
            text[:length]
        )

    def description_display(self, obj):
        return self.truncate_text(obj.description)
    description_display.short_description = 'Description'

    def full_name_display(self, obj):
        name = self.truncate_text(obj.full_name.title() if obj.full_name else "-")
        return format_html(
                '<strong>{}</strong>',
                name
            )
    full_name_display.short_description = 'Full Name'

    def job_title_display(self, obj):
        return self.truncate_text(obj.job_title.title() if obj.job_title else "-")
    job_title_display.short_description = 'Job Title'

    def company_name_display(self, obj):
        return self.truncate_text(obj.company_name.title() if obj.company_name else "-")
    company_name_display.short_description = 'Company'

    def industry_name_display(self, obj):
        return self.truncate_text(obj.industry_name.title() if obj.industry_name else "-")
    industry_name_display.short_description = 'Industry'

    def company_country_name_display(self, obj):
        return self.truncate_text(obj.company_country_name.title() if obj.company_country_name else "-")
    company_country_name_display.short_description = 'Country'

    def company_domain_display(self, obj):
        if obj.company_domain:
            domain = self.truncate_text(obj.company_domain)
            return format_html(
                '<a href="https://{}" target="_blank" title="{}">{}</a>',
                obj.company_domain,
                obj.company_domain,
                domain
            )
        return "-"
    company_domain_display.short_description = 'Domain'

    def company_linkedin_url_display(self, obj):
        if obj.company_linkedin_url:
            return format_html(
                '<a href="{}" target="_blank" title="{}">'
                '<img src="/static/admin/images/linkedin_icon.svg" '
                'width="24" height="24" style="vertical-align: middle;">'
                '</a>',
                obj.company_linkedin_url,
                obj.company_linkedin_url
            )
        return "-"


    def linkedin_url_display(self, obj):
        if obj.linkedin_url:
            return format_html(
                '<a href="{}" target="_blank" title="{}">'
                '<img src="/static/admin/images/linkedin_icon.svg" '
                'width="24" height="24" style="vertical-align: middle;">'
                '</a>',
                obj.linkedin_url,
                obj.linkedin_url
            )
        return "-"

    def company_logo_display(self, obj):
        if obj.company_logo:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: contain;" />', obj.company_logo)
        return "-"
    
    def additional_personal_emails_display(self, obj):
        if not obj.additional_personal_emails:
            return ""
        try:
            emails = eval(obj.additional_personal_emails) if isinstance(obj.additional_personal_emails, str) else obj.additional_personal_emails
            masked_emails = [self.mask_email(email) for email in emails]
            full_text = ", ".join(masked_emails)
            return self.truncate_text(full_text)
        except:
            return ""
    additional_personal_emails_display.short_description = 'Other Emails'

    def mask_email(self, email):
        if not email:
            return "-"
        try:
            username, domain = email.split('@')
            domain_name, tld = domain.rsplit('.', 1)
            masked_length = random.randint(5, 9)
            return f"{username[0]}{'*' * masked_length}@*****.{tld}"
        except ValueError:
            return email

    def mask_phone(self, phone):
        if not phone:
            return "-"
        clean_phone = ''.join(filter(str.isdigit, phone))
        if len(clean_phone) >= 6:
            return f"{clean_phone[0]}{'*' * 8}{clean_phone[-2:]}"
        return f"{'*' * len(clean_phone)}"

    def business_email_display(self, obj):
        return self.mask_email(obj.business_email)

    def mobile_phone_display(self, obj):
        return self.mask_phone(obj.mobile_phone)

    def company_phone_display(self, obj):
        return self.mask_phone(obj.company_phone)

    def personal_phone_display(self, obj):
        return self.mask_phone(obj.personal_phone)

    search_fields = (
        'full_name', 'business_email', 'additional_personal_emails',
        'company_name', 'job_title', 'industry_name'
    )


    # Add short_description to each display method
    company_logo_display.short_description = ''
    company_linkedin_url_display.short_description = 'Company LinkedIn'
    linkedin_url_display.short_description = 'Person LinkedIn'
    company_phone_display.short_description = 'Company Phone'
    description_display.short_description = 'Description'

    full_name_display.short_description = 'Name'
    business_email_display.short_description = 'Email'
    mobile_phone_display.short_description = 'Mobile'
    personal_phone_display.short_description = 'Personal'
    additional_personal_emails_display.short_description = 'Other Emails'

    list_filter = (
        IndustryFilter,
        CountryFilter,
        EmployeesRangeFilter
    )
    
    # Optional: Enable filter submit button like in the example
    list_filter_submit = True

    list_per_page = 50
    list_display_links = None  # This removes the clickable links
    
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True  # Only allow viewing

    def get_queryset(self, request):
        print("\n" + "="*50)
        print("DEBUG: Entering get_queryset")
        print(f"DEBUG: Request GET params: {dict(request.GET)}")
        allowed_params = {'industry_name', 'company_country_name', 'employees_range', 'p'}  # 'p' for pagination
        request.GET = request.GET.copy()
        for key in list(request.GET.keys()):
            if key not in allowed_params:
                del request.GET[key]
        try:
            # Get all active filters
            filters = {}
            for filter_key in ['industry_name', 'company_country_name', 'employees_range']:
                filter_values = request.GET.getlist(filter_key)  # Use getlist instead of get
                if filter_values:
                    filters[filter_key] = filter_values  # Pass the entire list of values

            # Get the page number and calculate offset for BigQuery
            try:
                page_num = int(request.GET.get('p', '1'))
            except ValueError:
                page_num = 1
            
            page_size = self.list_per_page
            offset = (page_num - 1) * page_size

            print(f"DEBUG: Pagination details:")
            print(f"  - Page number: {page_num}")
            print(f"  - Page size: {page_size}")
            print(f"  - Calculated offset: {offset}")
            
            # Fetch exactly the page we need from BigQuery
            results = fetch_contacts(
                filters=filters,  # Pass all filters at once
                limit=page_size,
                offset=offset,
                order_by='created_at DESC'
            )
            
            print(f"DEBUG: Query returned {len(results)} results")
            if results:
                print(f"DEBUG: First result ID: {results[0].get('id')}")
                print(f"DEBUG: Last result ID: {results[-1].get('id')}")
            
            instances = [BigQueryContact(**r) for r in results]
            return BigQueryQuerySet(instances=instances)
            
        except Exception as e:
            print(f"DEBUG ERROR: {str(e)}")
            logger.error(f"Error in get_queryset: {str(e)}", exc_info=True)
            raise

    def get_paginator(self, request, queryset, per_page, orphans=0, allow_empty_first_page=True):
        paginator = Paginator(queryset, per_page)
        paginator.count = 7000000
        return paginator

    def changelist_view(self, request, extra_context=None):
        print("DEBUG: Entering changelist_view")
        try:
            response = super().changelist_view(request, extra_context=extra_context)
            print("DEBUG: Successfully generated changelist view")
            return response
        except Exception as e:
            print(f"DEBUG: Error in changelist_view: {str(e)}")
            logger.error(f"Error in changelist_view: {str(e)}", exc_info=True)
            raise

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

# Register the model and its admin
admin.site.register(BigQueryContact, BigQueryContactAdmin)
