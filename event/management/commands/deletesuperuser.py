from event.models import User
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)

    def handle(self, *args, **options):
        try:
            user = User.objects.get(username=options['username'])
            print(user)
        except User.DoesNotExist:
            raise CommandError("There is no user named {}".format(options['username']))

        self.stdout.write("-------------------")
        self.stdout.write("Deleting superuser {}".format(options.get('username')))
        user.delete()
        self.stdout.write("Done.")