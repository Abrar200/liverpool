from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from django.db.models.manager import Manager
import datetime
from PIL import Image


class Players(models.Model):
	name = models.CharField(max_length=255)
	position = models.CharField(max_length=255)
	bio = models.TextField()
	image_url = models.CharField(max_length=2083)

	def __str__(self):
		return '%s' % (self.name)


class News(models.Model):
	author = models.CharField(max_length=255, null=True)
	title = models.CharField(max_length=255)
	image = models.ImageField(upload_to='images', null=True)
	summary = models.CharField(max_length=3000, null=True)
	description = models.CharField(max_length=3000000000000000000000000000000000000000000000000000000000000000000000)
	date_posted = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return '%s' % (self.title)

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		img = Image.open(self.image.path)

		if img.height > 800 or img.width > 450:
			output_size = (800, 450)
			img.thumbnail(output_size)
			img.save(self.image.path)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=255)
    def __str__(self):
        return f'{self.user.username} Profile'


    def save(self, *args, **kwargs):
    	super().save(*args, **kwargs)


class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	news = models.ForeignKey(News, related_name="comments", on_delete=models.CASCADE)
	body = models.CharField(max_length=3000000000000000000000000000000000000000000000000000000000000000000000)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return '%s - %s' % (self.news.title, self.user.username)
