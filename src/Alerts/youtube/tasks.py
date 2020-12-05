from __future__ import absolute_import, unicode_literals
from utils import parseDateTime
from celery import shared_task
from .youtubeBot import youtubeScraper
from .models import YoutubeNotification

@shared_task
def getUserNotifications():
	notifications  = youtubeScraper().getNotifications()
	
	for notification in notifications:
		qs = YoutubeNotification.objects.filter(videoLink = notification['videoLink'])
		if not qs:
			notification['time'] = parseDateTime(notification['time'])
			YoutubeNotification(**notification).save()
	

