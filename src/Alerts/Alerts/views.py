from django.shortcuts import render, reverse, redirect
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from reddit.models import RedditPost
from medium.models import MediumNotification
from youtube.models import YoutubeNotification
from linkedIn.models import LinkedInPost

def home(request):
	return redirect(reverse('reddit:home'))

@require_http_methods(['POST'])
def search(request):
	querry = request.POST.get('querry')
	youtubeLookup = (Q(description__contains = querry))
	mediumLookup = (Q(description__contains = querry))
	linkedInLookup = (Q(body__contains = querry))
	redditLookup = (Q(title__contains = querry)| Q(body__contains = querry) | Q(subreddit__contains = querry))

	qsYoutube = YoutubeNotification.objects.filter(youtubeLookup).distinct()
	qsMedium = MediumNotification.objects.filter(mediumLookup).distinct()
	qsLinkedIn = LinkedInPost.objects.filter(linkedInLookup).distinct()
	qsReddit = RedditPost.objects.filter(redditLookup).distinct()
	context = {}
	context['youtube'] = qsYoutube
	context['medium'] = qsMedium
	context['reddit'] = qsReddit
	context['linkedIn'] = qsLinkedIn
	context['querry'] = querry
	return render(request, "searchResults.html",context)
