from django.db import models

# Create your models here.


class ExcelImport(models.Model):
	name = models.CharField(max_length=50)
	file =  models.FileField(upload_to = "excel/")
	date = models.DateTimeField(auto_now=True)
	check = models.BooleanField(default=False, db_index=True, verbose_name='Проверрено')
	only_old = models.BooleanField(default=False, db_index=True, verbose_name='Только обновить имеющийся позиции')

	code = models.IntegerField(default=1, null=True, blank=True, verbose_name='Код')
	articul = models.IntegerField(default=3, null=True, blank=True, verbose_name='Артикул')
	producer = models.IntegerField(default=2, null=True, blank=True, verbose_name='Производитель')
	description = models.IntegerField(default=4, null=True, blank=True, verbose_name='Описание')
	stock = models.IntegerField(default=5, null=True, blank=True, verbose_name='Количество')
	
	filter_one = models.IntegerField(null=True, blank=True, verbose_name='фильтр ур. 1')
	filter_two = models.IntegerField(null=True, blank=True, verbose_name='фильтр ур. 2')
	filter_three = models.IntegerField(null=True, blank=True, verbose_name='фильтр ур. 3')
	filter_four = models.IntegerField(null=True, blank=True, verbose_name='фильтр ур. 4')
	filter_five = models.IntegerField(null=True, blank=True, verbose_name='фильтр ур. 5')
	
	price = models.IntegerField(default=6, null=True, blank=True, verbose_name='Цена')
	opt_0 = models.IntegerField(null=True, blank=True, verbose_name='опт 0')
	opt_1 = models.IntegerField(default=7, null=True, blank=True, verbose_name='опт 1')
	opt_2 = models.IntegerField(default=8, null=True, blank=True, verbose_name='опт 2')
	opt_3 = models.IntegerField(default=9, null=True, blank=True, verbose_name='опт 3')
	opt_4 = models.IntegerField(null=True, blank=True, verbose_name='опт 4')
	opt_5 = models.IntegerField(default=10, null=True, blank=True, verbose_name='опт 5')
	opt_6 = models.IntegerField(null=True, blank=True, verbose_name='опт 6')
	opt_7 = models.IntegerField(null=True, blank=True, verbose_name='отп 7')
	opt_8 = models.IntegerField(null=True, blank=True, verbose_name='отп 8')
	opt_9 = models.IntegerField(null=True, blank=True, verbose_name='отп 9')
	opt_10 = models.IntegerField(null=True, blank=True, verbose_name='отп 10')
	opt_11 = models.IntegerField(null=True, blank=True, verbose_name='отп 11')
	opt_12 = models.IntegerField(null=True, blank=True, verbose_name='отп 12')
	opt_13 = models.IntegerField(null=True, blank=True, verbose_name='опт 13')
	opt_14 = models.IntegerField(null=True, blank=True, verbose_name='опт 14')
	opt_15 = models.IntegerField(null=True, blank=True, verbose_name='опт 15')
	opt_16 = models.IntegerField(null=True, blank=True, verbose_name='опт 16')
	opt_17 = models.IntegerField(null=True, blank=True, verbose_name='опт 17')
	opt_18 = models.IntegerField(null=True, blank=True, verbose_name='опт 18')
	opt_19 = models.IntegerField(null=True, blank=True, verbose_name='отп 19')
	opt_20 = models.IntegerField(null=True, blank=True, verbose_name='опт 20')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Загрузить_эксел'
		verbose_name_plural = 'Загрузить_эксели'
	


class BannerStock(models.Model):
	name = models.CharField(max_length=50, blank=True, null=True)
	date =  models.DateTimeField(auto_now=True, editable=True,)
	img =  models.ImageField(upload_to = "banner/")
	visibility = models.BooleanField(default=True, db_index=True, verbose_name='Видимость')

	def __str__(self):
		return self.name


	class Meta:
		verbose_name = 'Баннер_акций'
		verbose_name_plural = 'Баннеры_акций'	


class PdfCatalogs(models.Model):
	name = models.CharField(max_length=50, blank=True, null=True)
	date =  models.DateTimeField(auto_now=True, editable=True,)
	img =  models.ImageField(upload_to = "pdf/pdf_img/")
	file = models.FileField(upload_to = "pdf/pdf_catalog/")
	visibility = models.BooleanField(default=True, db_index=True, verbose_name='Видимость')

	def __str__(self):
		return self.name


	class Meta:
		verbose_name = 'Каталог_PDF'
		verbose_name_plural = 'Каталоги_PDF'	
