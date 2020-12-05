from django.db import models
import markdown

# Create your models here.

class LinkedInPost(models.Model):
	image = models.TextField()
	body = models.TextField()
	created = models.DateTimeField()
	url = models.TextField()
	read = models.BooleanField(default = False)

	class Meta:
		ordering = ['-created']

	def __str__(self):
		return self.body[:50]

	def mark(self):
		return markdown.markdown(self.body)

	def markWithoutP(self):
		p = '<p>'
		np = '</p>'
		md = markdown.markdown(self.body)
		if md.startswith(p) and md.endswith(np): 
		    md = md[len(p):-len(np)]
		return md
		
	def makeUrl(self):
		return "https://linkedIn.com" + self.url

	def getAndUpdateReadStatus(self):
		curr = self.read
		self.read = True
		self.save()
		return curr