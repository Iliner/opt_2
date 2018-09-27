# from django.db import models
# from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model
# from main_page.models import Goods
# # Create your models here.

# # User = get_user_model()
# # class Profile(models.Model):
# # 	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
# # 	ebooks = models.ManyToManyField(Goods, blank=True)

# # 	def __str__(self):
# # 		return self.user.username	


# class CartItem(models.Model):
# 	product = models.ForeignKey(Goods)
# 	count = models.PositiveIntegerField()
# 	item_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
# 	customer = models.ForeignKey('Customer', default=None)

# 	def item_tootal_count(self):
# 		return int(self.count) * int(self.product.price)

# 	def __unicode__(self):
# 		return "Car item for product {}".format(self.product.code)

# 	def __str__(self):
# 		return "pk-{} {} {} {}".format(self.pk, self.product.code, self.count, self.item_total)


# class Cart(models.Model):
# 	items = models.ManyToManyField(CartItem)
# 	cart_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
# 	paid_for = models.BooleanField(default=False, db_index=True, verbose_name='Оплаченно')
# 	date = models.DateTimeField(auto_now=True)

# 	def cart_total_summ(self):
# 		summ = 0
# 		for item in self.items.all():
# 			summ += item.item_total
# 		return summ


# 	# def cart_total_delete(self, code):
# 	# 	need_item = self.items.get(product__code=code)
# 	# 	need_item.item_total 
		



# 	def __str__(self):
# 		return str(self.id)	






# OPTS = (
# 	(1, 1),
# 	(2, 2),
# 	(3, 3),
# 	(5, 6),
# 	(6, 6),
# 	)


# class Customer(models.Model):
# 	user = models.ForeignKey(User, on_delete=models.CASCADE)
# 	baskets = models.ManyToManyField(Cart, blank=True)
# 	opt = models.IntegerField(choices=OPTS , default=1)

# 	def __str__(self):
# 		return "{} {}, отп: {}".format(self.user.first_name, self.user.last_name, self.opt)

# 	class Meta:
# 		verbose_name = 'Клиент'
# 		verbose_name_plural = 'Клиенты'