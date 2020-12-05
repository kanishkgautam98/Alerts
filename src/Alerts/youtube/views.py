from django.shortcuts import render
from .tasks import getUserNotifications
from .models import YoutubeNotification
# Create your views here.
def home(request):
	#getUserNotifications.delay()
	qs = YoutubeNotification.objects.all()
		
	return render(request, "youtube/home.html", {"youtubeNotifications": qs})