from django.utils.html import format_html
from django.contrib import admin
from .bigquery import fetch_contacts, get_unique_values, get_filtered_count
from django.db import models
import logging
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.db.models.sql import Query
import random
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.core.cache import cache
from unfold.admin import ModelAdmin  # Change this import
from unfold.contrib.filters.admin import DropdownFilter, MultipleDropdownFilter
from django.utils.translation import gettext_lazy as _
from .models import ContactList, Contact
from django.utils.text import slugify
from django.shortcuts import redirect
from django.urls import path
from django.utils import timezone
from django.template.response import TemplateResponse
from django.contrib.admin.views.main import ChangeList

EMPTY_VALUES = (None, '')

logger = logging.getLogger(__name__)

class ContactListAdmin(ModelAdmin):
    list_display = ('title', 'contact_count', 'updated_at', 'view_contacts_link')
    search_fields = ('title',)
    readonly_fields = ('created_at', 'updated_at', 'contact_count' )
    fields = ('title', 'contact_ids', 'contact_count', 'updated_at')
    
    # Explicitly set no filters to prevent BigQuery queries
    list_filter = []
    
    # Disable the filter sidebar completely
    list_filter_submit = False
    
    def view_contacts_link(self, obj):
        url = reverse('admin:filter-by-list', args=[obj.id])
        return format_html('<a href="{}">View Contacts</a>', url)
    view_contacts_link.short_description = 'Contacts'

    def response_change(self, request, obj):
        # Redirect to the filter-by-list view after saving a ContactList
        return HttpResponseRedirect(reverse('admin:filter-by-list', args=[obj.pk]))

    def change_view(self, request, object_id, form_url='', extra_context=None):
        # Redirect to the filter-by-list view instead of showing the change form
        return HttpResponseRedirect(reverse('filter-by-list', args=[object_id]))

# Register the model and its admin
admin.site.register(ContactList, ContactListAdmin)

class ContactAdmin(ModelAdmin):
    list_display = (
        'full_name_display',
        'company_logo_display',
        'company_name_display',
        'job_title_display',
        'industry_name_display',
        'company_linkedin_url_display',
        'company_domain_display',
        'linkedin_url_display',
        'company_country_name_display',
        'employees_range',
        'description_display',
    )

    actions = ['export_selected_contacts']

    def export_selected_contacts(self, request, queryset):
        selected_ids = [obj.contact_id for obj in queryset]
        
        # Create a new ContactList with the selected IDs
        contact_list = ContactList.objects.create(
            title=f"Exported Contacts {timezone.now().strftime('%Y-%m-%d %H:%M')}",
            user=request.user,
            contact_ids=selected_ids
        )
        
        self.message_user(request, f"Added {len(selected_ids)} contacts to {contact_list.title}.")
        
        # Redirect to the newly created ContactList's change page
        return HttpResponseRedirect(reverse('admin:app_contactlist_change', args=[contact_list.id]))
    export_selected_contacts.short_description = "Export selected contacts"

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
            '<div class="row-selector" data-id="{}" style="cursor: pointer;">'
            '<strong>{}</strong>'
            '</div>',
            obj.contact_id,
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
    company_linkedin_url_display.short_description = 'Company LinkedIn'
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
    linkedin_url_display.short_description = 'Person LinkedIn'
    def company_logo_display(self, obj):
        if obj.company_logo:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: contain;" />', obj.company_logo)
        return "-"
    company_logo_display.short_description = ''
    search_fields = (
        'full_name',
        'company_name', 'job_title', 'industry_name'
    )

    list_filter = (
        'industry_name',
        'company_country_name',
        'employees_range'
    )
    
    list_filter_submit = True
    list_per_page = 50
    
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('filter-by-list/<int:list_id>/', self.admin_site.admin_view(self.filter_by_list), name='filter-by-list'),
        ]
        return custom_urls + urls

    def filter_by_list(self, request, list_id):
        contact_list = ContactList.objects.get(id=list_id)
        contact_ids = contact_list.contact_ids

        # Debugging: Print or log the contact_ids
        print("Filtering contacts with IDs:", contact_ids)

        # Ensure the queryset is filtered correctly
        queryset = self.get_queryset(request).filter(contact_id__in=contact_ids)

        # Debugging: Print or log the filtered queryset
        print("Filtered queryset count:", queryset.count())

        # Create a ChangeList instance with the required parameters
        cl = ChangeList(
            request, self.model, self.list_display, self.list_display_links,
            self.list_filter, self.date_hierarchy, self.search_fields,
            self.list_select_related, self.list_per_page, self.list_max_show_all,
            self.list_editable, self, self.sortable_by, self.search_help_text
        )
        cl.formset = None
        cl.queryset = queryset

        # Manually set the result_list and result_count to the filtered queryset
        cl.result_list = queryset
        cl.result_count = queryset.count()  # Set the correct count for pagination
        cl.full_result_count = queryset.count()  # Set the full count for pagination

        # Ensure paginator is aware of the filtered queryset
        cl.paginator = cl.model_admin.get_paginator(request, queryset, cl.list_per_page)

        # Use the custom template to display the filtered contacts
        context = dict(
            self.admin_site.each_context(request),
            title=f"Contacts in {contact_list.title}",
            cl=cl,
            opts=self.model._meta,
            media=self.media,
        )
        return TemplateResponse(request, "admin/change_list.html", context)

    class Media:
        css = {
            'all': (
                'admin/css/custom_admin.css',
                'admin/css/vendor/select2/select2.css',
                'admin/css/autocomplete.css',
            )
        }
        js = (
            'admin/js/vendor/jquery/jquery.js',
            'admin/js/vendor/select2/select2.full.js',
            'admin/js/jquery.init.js',
            'admin/js/core.js',
            '/jsi18n/',
            'unfold/js/select2.init.js',
            'admin/js/admin/RelatedObjectLookups.js',
            'admin/js/actions.js',
            'admin/js/urlify.js',
            'admin/js/prepopulate.js',
            'admin/js/vendor/xregexp/xregexp.js',
            'admin/js/row_selection.js',
        )

# Register the model and its admin
admin.site.register(Contact, ContactAdmin)