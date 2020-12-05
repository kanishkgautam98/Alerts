from django.db import models

# Create your models here.
class MediumNotification(models.Model):
	description = models.TextField()
	image = models.TextField()
	date = models.DateTimeField()

	class Meta:
		ordering = ['-date']

	def __str__(self):
		return self.description