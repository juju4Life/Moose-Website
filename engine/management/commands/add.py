from django.core.management.base import BaseCommand
from django.core.management import call_command

def load_fixture(n):
	call_command('loaddata', '{}.json'.format(str(n)))

class Command(BaseCommand):
    def handle(self, **options):
    	current = int(input('Start:\n>'))
    	stop = int(input('Stop:\n>'))
    	while current <= stop:
    		load_fixture(current)
    		current += 1
    		print(current-1)

        
