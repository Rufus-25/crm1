#from django.db.utils import IntegrityError
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User, Group
from .models import Customer

'''
@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        try:
            group = Group.objects.get(name='customer')
            instance.groups.add(group)
            if not Customer.objects.filter(user=instance).exists():
                Customer.objects.create(
                    user=instance,
                    name=instance.username
                )
                print("Customer created!")
            else:
                print("Customer already exists for this user.")
        except IntegrityError as e:
            print(f"IntegrityError: {e}")
        except Group.DoesNotExist:
            print("Customer group does not exist!")

#post_save.connect(create_customer, sender=User)
'''

@receiver(post_save, sender=User)
def update_customer(sender, instance, created, **kwargs):
    if created == False:
        print("Customer updated")

@receiver(post_save, sender=Customer)
def update_customer_details(sender, instance, created, **kwargs):
    if created == False:
        this_customer_name = instance.name
        print(f"{this_customer_name} profile updated internally.")