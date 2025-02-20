from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group, Permission
from django.db import transaction

@receiver(post_save, sender=User)
def setup_user_access(sender, instance, created, **kwargs):
    if created:  # only when user is created
        with transaction.atomic():
            # Make user staff so they can access admin
            instance.is_staff = True
            
            # Get or create the customer group
            customer_group, created = Group.objects.get_or_create(name='Customers')
            
            if created:  # If the group was just created, set up permissions
                # Example: Allow viewing contacts but not editing/deleting
                view_contact = Permission.objects.get(
                    codename='view_bigquerycontact',
                    content_type__app_label='app',
                    content_type__model='bigquerycontact'
                )
                customer_group.permissions.add(view_contact)
            
            # Add user to the customer group
            instance.groups.add(customer_group)
            instance.save() 