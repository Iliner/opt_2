from django.db import models

# Create your models here.


class ExcelImport(models.Model):
	name = models.CharField(max_length=50)
	file =  models.FileField(upload_to = "excel/")
	date = models.DateTimeField(auto_now=True)
	check = models.BooleanField(default=False, db_index=True, verbose_name='Проверрено')

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
