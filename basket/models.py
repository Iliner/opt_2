from django.db import models
from django.contrib.auth import get_user_model
from main_page.models import Goods
# Create your models here.

# User = get_user_model()
# class Profile(models.Model):
# 	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
# 	ebooks = models.ManyToManyField(Goods, blank=True)

# 	def __str__(self):
# 		return self.user.username	


class CartItem(models.Model):
	product = models.ForeignKey(Goods)
	count = models.PositiveIntegerField()
	item_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

	def __unicode__(self):
		return "Car item for product {}".format(self.product.code)

	def __str__(self):
		return "{} {} {}".format(self.product.code, self.count, self.item_total)

class Cart(models.Model):
	items = models.ManyToManyField(CartItem)
	cart_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

	def __str__(self):
		return str(self.id)	
