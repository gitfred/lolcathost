from django.contrib import admin
from embed_video.admin import AdminVideoMixin

from files.models import YouTubeMusic


@admin.register(YouTubeMusic)
class YouTubeMusicAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass
