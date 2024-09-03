from django.core.management import BaseCommand
from django.db.migrations.recorder import MigrationRecorder


class Command(BaseCommand):
    """ Use the command before migrations only when you plan
    to make one migration file for each application """

    def handle(self, *args, **options):
        print(f'Truncate these all apps from django_migrations table')
        migrations = MigrationRecorder.Migration.objects.all()
        print('such migrations are found: ')
        for migration in migrations:
            print(migration.app, migration.name)
        try:
            migrations.delete()
            print('Truncate success')
        except Exception as error:
            print(error)
