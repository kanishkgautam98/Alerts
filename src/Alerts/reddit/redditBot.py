import praw
from django.conf import settings
config = settings.CONFIG
from .models import RedditPost
from prawcore import NotFound

class RedditBot:
    def __init__(self):
        self.clientId = config.get('reddit').get('clientId')
        self.clientSecret = config.get('reddit').get('clientSecret')
        self.userAgent = config.get('reddit').get('userAgent')
        self.crawler = praw.Reddit(client_id = self.clientId, client_secret = self.clientSecret, user_agent = self.userAgent)
        
    def crawl(self, subreddit):
        pass
    
    def hot(self, subreddit = "learnpython", limit=10):        
        for submission in self.crawler.subreddit(subreddit).hot(limit=limit):
            qs = RedditPost.objects.filter(postId = submission.id)
            if not qs:
                newPost = RedditPost()
                newPost.title = submission.title
                newPost.body = submission.selftext
                newPost.createdDate = submission.created
                newPost.url = submission.url
                newPost.comments = submission.num_comments
                newPost.postId = submission.id
                newPost.subreddit = subreddit
                newPost.save()
        
    def checkSubreddit(self, subreddit):
        exists = True
        try:
            self.crawler.subreddits.search_by_name(subreddit, exact=True)
        except NotFound:
            exists = False
        return exists