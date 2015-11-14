from subprocess import PIPE
from subprocess import Popen
import os

from django.conf import settings
from django.core.files import File
from django.db import models
from embed_video.fields import EmbedVideoField
from filer.fields.file import FilerFileField
from filer.models import File as FileFilerModel
import youtube_dl


class DownloadError(Exception):

    def __init__(self, message):
        self.message = message


class YouTubeMusic(models.Model):
    url = EmbedVideoField()
    title = models.CharField(max_length=100, blank=True, null=True)
    result = models.TextField(blank=True, null=True)
    file = FilerFileField(blank=True, null=True)

    def __str__(self):
        return self.title or ''

    def download(self, ext='mp3'):
        ydl = youtube_dl.YoutubeDL(settings.DOWNLOAD_OPTIONS)

        with ydl:
            info = ydl.extract_info(self.url, download=False)

        self.title = info['title']

        arg_file = "{}.%(ext)s".format(info['id'])
        name_w_ext = arg_file % {'ext': ext}
        process = Popen(
            [
                'youtube-dl',
                '--extract-audio',
                '--audio-format', ext,
                '--audio-quality', '0',  # the best
                '-o', arg_file,
                self.url,
            ],
            stdout=PIPE, stderr=PIPE)

        stdout, stderr = process.communicate()
        self.result = "stdout:{}\n\nstderr:{}".format(stdout, stderr)
        if stderr:
            self.save()
            raise DownloadError(stderr)

        with open(name_w_ext, 'rb') as fp:
            django_file = File(fp, name=self.title + '.{}'.format(ext))
            self.file = FileFilerModel.objects.create(
                name=self.title,
                file=django_file)

        os.remove(name_w_ext)
        self.save()
