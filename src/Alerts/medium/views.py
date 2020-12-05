from django.shortcuts import render
from .tasks import getUserNotifications
from .mediumBot import ScraperPersonal
from .models import MediumNotification
# Create your views here.
def home(request):
	# getUserNotifications.delay()
	qs = MediumNotification.objects.all()
	return render(request, 'medium/home.html', {'mediumNotifications': qs})