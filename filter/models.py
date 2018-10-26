from django.db import models

# Create your models here.



class LvlOne(models.Model):
	name = models.CharField(max_length=100, verbose_name='уровень: 1')
	next_lvl = models.ManyToManyField("LvlTwo", blank=True, verbose_name='связь со следующим уровнем')


	def __str__(self):
		return "{}".format(self.name)

	class Meta:
		ordering = ['name']
		verbose_name_plural = 'Уровень: 1'

class LvlTwo(models.Model):
	name = models.CharField(max_length=100, verbose_name='уровень: 2')
	next_lvl = models.ManyToManyField("LvlThree", blank=True, verbose_name='связь со следующим уровнем')


	def __str__(self):
		return "{}".format(self.name)

	class Meta:
		ordering = ['name']
		verbose_name_plural = 'Уровень: 2'


class LvlThree(models.Model):
	name = models.CharField(max_length=100, verbose_name='уровень: 3')
	next_lvl = models.ManyToManyField("LvlFour", blank=True, verbose_name='связь со следующим уровнем')


	def __str__(self):
		return "{}".format(self.name)
		
	class Meta:
		ordering = ['name']
		verbose_name_plural = 'Уровень: 3'


class LvlFour(models.Model):
	name = models.CharField(max_length=100, verbose_name='уровень: 4')
	next_lvl = models.ManyToManyField("LvlFive", blank=True, verbose_name='связь со следующим уровнем')


	def __str__(self):
		return "{}".format(self.name)
		
	class Meta:
		ordering = ['name']
		verbose_name_plural = 'Уровень: 4'

class LvlFive(models.Model):
	name = models.CharField(max_length=100, verbose_name='уровень: 5')


	def __str__(self):
		return "{}".format(self.name)
		
	class Meta:
		ordering = ['name']
		verbose_name_plural = 'Уровень: 5'