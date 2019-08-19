from django.contrib import admin
from .models import FeedSubmission


@admin.register(FeedSubmission)
class FeedsSubmissionAdmin(admin.ModelAdmin):
    list_display = ['feed_id', 'success', 'feed_created_on', 'feed_successful_on', ]


