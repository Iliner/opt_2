from django.db import models
#from basket.models import Cart
from django.contrib.auth.models import User

# Create your models here.





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