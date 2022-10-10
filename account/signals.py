from django.contrib.auth.models import Group
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from account.models import User

@receiver(post_save, sender=User, dispatch_uid='create_user_groups_signal')
def create_user_groups(sender, instance, created, **kwargs):
    if created and instance.role and not instance.is_superuser:
        Group.objects.get(name=instance.role).user_set.add(instance)