from django.shortcuts import render, reverse, redirect
import markdown
# Create your views here.
from .models import RedditPost, Pending
from .redditBot import RedditBot
from .tasks import checkExistance
from django.contrib import messages
from django.views.decorators.http import require_http_methods


def getDistinctSubreddits():
	return RedditPost.objects.order_by('subreddit').values_list('subreddit', flat = True).distinct()


def home(request, subreddit = None):
	#default subreddit is learnpython
	if subreddit is None:
		return redirect(reverse('reddit:home', kwargs={'subreddit':"learnpython"}))
	subreddits = getDistinctSubreddits()

	qs = RedditPost.objects.filter(subreddit = subreddit)
	return render(request, "reddit/home.html", {'redditPosts' : qs, 'subreddits': subreddits, 'subreddit' : subreddit, 'pending' : Pending.objects.all()})

@require_http_methods(['POST'])
def new(request):
	subreddit = request.POST.get('subreddit')
	curr = request.POST.get('current').strip()
	#check for empty submission
	if not subreddit:
		messages.error(request,'Please enter something')
		return redirect(reverse('reddit:home'))
	
	#Check for preexistance of subreddit
	if RedditPost.objects.filter(subreddit = subreddit):
		messages.error(request, r'The subreddit <b>%s</b> already exists'%subreddit)
		return redirect(reverse('reddit:home', kwargs={'subreddit': curr}))
	
	#Check if subreddit is already added as pending
	if not Pending.objects.filter(subreddit = subreddit):
		Pending(subreddit = subreddit).save()
		checkExistance.delay(subreddit)
		messages.success(request, r'Your request is under process...If the subreddit <b>%s</b> exists, it shall be added'%subreddit)
	else:
		messages.error(request,'Your request for the subreddit <b>%s</b> is already in pending'%subreddit)

	return redirect(reverse('reddit:home', kwargs={'subreddit': curr}))


def remove(request):
	if request.POST:
		subreddits = request.POST.getlist('subreddit')
		if len(subreddits) is 0:
			messages.error(request, 'Please select atleast one subreddit')
		else :
			for subreddit in subreddits:
				RedditPost.objects.filter(subreddit = subreddit).delete()
			messages.success(request, 'Successfully removed the selected subreddits')
		
		return redirect(reverse('reddit:home'))
	#default reddit is learnpython and so it cannot be removed	
	subreddits = list(getDistinctSubreddits())
	subreddits.remove('learnpython')

	if not subreddits:
		messages.error(request, "No subreddit to be removed...Please add some first")
		return redirect(reverse('reddit:home'))
	return render(request, "reddit/removeSubreddit.html", {'subreddits' : subreddits})
