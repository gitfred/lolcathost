from django.core.management.base import BaseCommand

from files.models import YouTubeMusic
from files.models import DownloadError


class Command(BaseCommand):
    help = "Ściąganie muzyki"

    def handle(self, *args, **options):
        for obj in YouTubeMusic.objects.filter(file__isnull=True):
            try:
                obj.download()
            except DownloadError as err:
                self.stderr.write(
                    "Nie ściągnięto: {}\nMSG:{}".format(obj.title, err.message))
            else:
                self.stdout.write("Ściągnięto: {}".format(obj.title))
