from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from .admin import BigQueryContactAdmin, BigQueryContact
from django.contrib import admin

# Create your views here.

@method_decorator(staff_member_required, name='dispatch')
class ContactsView(View):
    def get(self, request, *args, **kwargs):
        # Create an instance of the admin class
        model_admin = BigQueryContactAdmin(BigQueryContact, admin.site)
        # Call the changelist view
        return model_admin.changelist_view(request)
