from django.db import models
import markdown 

# Create your models here.
class RedditPost(models.Model):
	title = models.TextField()
	body = models.TextField()
	comments = models.IntegerField()
	createdDate = models.DateField(auto_now_add = True)
	url = models.TextField()
	postId = models.CharField(max_length = 20)
	subreddit = models.CharField(max_length = 50)
	
	class Meta:
		ordering = ['-createdDate']	

	def __str__(self):
		return self.title


	def mark(self):
		return markdown.markdown(self.body)

class Pending(models.Model):
	subreddit = models.TextField()

	def __str__(self):
		return self.subreddit
