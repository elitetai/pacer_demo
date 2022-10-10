from django.core.management import call_command
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Script to run models' makemigrations and migrate"

    def add_arguments(self, parser):
        parser.add_argument(
            '--app',
            help="The specific app name to be migrated",
        )
    
    def run_makemigrations(self, app=None):
        if app:
            call_command('makemigrations', app)
        else:
            call_command('makemigrations')

    def run_migrate(self, app=None):
        if app:
            call_command('migrate', app)
        else:
            call_command('migrate')

    def handle(self,  *args, **options):
        app = options['app']
        print(f'Calling makemigrations...')
        self.run_makemigrations(app)
        print('\t...complete!!')
        print(f'Calling migrate...')
        self.run_migrate(app)
        print('\t...complete!!')