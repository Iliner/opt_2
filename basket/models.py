from django.db import models
from django.db.models.fields import PositiveSmallIntegerField
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

# Create your models here.



 


User = get_user_model()


class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	ebooks = models.ManyToManyField(Goods, blank=True)

	def __str__(self):
		return self.user.username

def post_save_profile_create(sender, instance, created, *args, **kwargs):
	if created:
		Profile.objects.get_or_create(user=instance)

post_save.connect(post_save_profile_create, sender=settings.AUTH_USER_MODEL)


class OrderItem(models.Model):
	"""
	Модель для добовление товара в корзину

	Это модель для добовление одной позиции в 
	общию корзину 
	"""
	good = models.OneToOneField(Goods, on_delete=models.SET_NULL, null=True)
	is_ordered = models.BooleanField(default=False)
	date_added = models.DateTimeField(auto_now=True)
	date_ordered = models.DateTimeField(null=True)


	def __str__(self):
		return self.good.code

	class Meta:
		verbose_name = 'штучный заказ'
		verbose_name_plural = 'штучные заказы'


class Order(models.Model):
	"""
	Модель общий корзины

	Модель куда будут входить все товары 
	которые заказали и уже тут рассчитываться 
	финальная стоймость заказа
	"""
	ref_code = models.CharField(max_length=15)
	owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
	is_ordered = models.BooleanField(default=False)
	items = models.ManyToManyField(OrderItem)
	date_ordered =  models.DateTimeField(auto_now=True)

	def get_cart_items(self):
		return self.items.all() 

	def get_cart_total(self):
		return sum([item.goods.price for item in self.items.all()])

	def __str__(self):
		return "{} - {}".format(self.owner, self.ref_code)