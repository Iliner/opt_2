from django.db import models

# Create your models here.


class SearchUserQuery(models.Model):
	query = models.PositiveIntegerField()
