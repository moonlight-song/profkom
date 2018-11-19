from django.db import models
from aldryn_newsblog.models import Article

class VkPost(models.Model):

	post_id = models.PositiveIntegerField()
	date = models.PositiveIntegerField()

	article = models.OneToOneField(Article)