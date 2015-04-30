from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Used to quickly add transactions.'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        
    def handle(self, *args, **options):
        dt = input('enter a date')
        print dt
        