from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from main_page.models import Goods
from decimal import Decimal



class CartItem(models.Model):
	product = models.ForeignKey(Goods)
	count = models.PositiveIntegerField()
	item_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
	customer = models.ForeignKey('Customer', default=None)
	price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)


	def price(self):
		return self.product.price

	def item_tootal_count(self):
		return int(self.count) * int(self.product.price)

	def __unicode__(self):
		return "Car item for product {}".format(self.product.code)

	def __str__(self):
		return "pk-{} {} {} {}".format(self.pk, self.product.code, self.count, self.item_total)


class Cart(models.Model):
	items = models.ManyToManyField(CartItem)
	cart_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
	paid_for = models.BooleanField(default=False, db_index=True, verbose_name='Оплаченно')
	date = models.DateTimeField(auto_now=True)

	def cart_total_summ(self):
		summ = Decimal()
		for item in self.items.all():
			print(item.item_total)
			summ += item.item_total
		print(summ)
		return summ


	# def cart_total_delete(self, code):
	# 	need_item = self.items.get(product__code=code)
	# 	need_item.item_total 
		



	def __str__(self):
		return str(self.id)	






OPTS = (
	(1, 1),
	(2, 2),
	(3, 3),
	(4, 4),
	(5, 5),
	(6, 6),
	(7, 7),
	(8, 8),
	(9, 9),
	(10, 10),
	(11, 11),
	(12, 12),
	(13, 13),
	(14, 14),
	(15, 15),
	(16, 16),
	(17, 17),
	(18, 18),
	(18, 18),
	(19, 12),
	)


class Customer(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	baskets = models.ManyToManyField(Cart, blank=True)
	opt = models.IntegerField(choices=OPTS , default=1)

	def __str__(self):
		return "{} {}, отп: {}".format(self.user.first_name, self.user.last_name, self.opt)

	class Meta:
		verbose_name = 'Клиент'
		verbose_name_plural = 'Клиенты'



class Manager(models.Model):
	first_name = models.CharField(max_length=30, verbose_name='Имя')
	last_name = models.CharField(max_length=30, verbose_name='Фамилия')
	third_name = models.CharField(max_length=30, null=True, blank=True, verbose_name='Отчество')
	mail_own = models.EmailField(null=True, blank=True, verbose_name='личная почта')
	mail_work = models.EmailField(null=True, blank=True, verbose_name='почта рабочая')
	phone_number_own = models.CharField(max_length=30, null=True, blank=True, verbose_name='личный номер тел')
	phone_number_work = models.CharField(max_length=30, null=True, blank=True, verbose_name='рабочий номер тел')
	customers = models.ManyToManyField(Customer,  blank=True, verbose_name='Клиенты')

	def __str__(self):
		return "{} {}".format(self.first_name, self.last_name)

	class Meta:
		verbose_name = 'Менеджер'
		verbose_name_plural = 'Менеджеры'