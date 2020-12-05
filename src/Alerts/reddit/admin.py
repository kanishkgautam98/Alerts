from django.contrib import admin
from .models import RedditPost,Pending
# Register your models here.
admin.site.register(RedditPost)
admin.site.register(Pending)