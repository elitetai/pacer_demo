from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from account.models import User

BASIC_USER_GROUP = User.BASIC_USER
BASIC_USER_MODEL = []
BASIC_USER_PERMISSION = ['view', 'add', 'delete', 'change']

PACER_SUPERADMIN_GROUP = User.PACER_SUPERADMIN
PACER_SUPERADMIN_MODEL = ['User', 'DailyRecord']
PACER_SUPERADMIN_PERMISSION = ['view', 'add', 'delete', 'change']

class Command(BaseCommand):
    help = 'Load initial permission data into DB'

    def create_group_and_permission(self, group, models, permissions):
        new_group, _ = Group.objects.get_or_create(name=group)
        new_group.permissions.clear()
        print('Assigning permissions to {}'.format(group))
        for model in models:
            for permission in permissions:
                codename = '{}_{}'.format(permission, slugify(model))
                print('\tCreating permission: {}'.format(codename))

                try:
                    model_add_perm = Permission.objects.get(codename=codename)
                except Permission.DoesNotExist:
                    print("\tPermission not found with codename '{}'".format(codename))
                else:
                    new_group.permissions.add(model_add_perm)
        print('Assigned Complete!')

    def handle(self, *args, **options):
        self.create_group_and_permission(BASIC_USER_GROUP, BASIC_USER_MODEL, BASIC_USER_PERMISSION)
        self.create_group_and_permission(PACER_SUPERADMIN_GROUP, PACER_SUPERADMIN_MODEL, PACER_SUPERADMIN_PERMISSION)
