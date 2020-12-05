from django.shortcuts import render

# Create your views here.
from .tasks import getUserNotifications
from .models import LinkedInPost
def home(request):
	# getUserNotifications.delay()
	qs = LinkedInPost.objects.all()
	return render(request, 'linkedIn/home.html', {'linkedInPosts': qs})