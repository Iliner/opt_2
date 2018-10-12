import os
import urllib.request
import urllib3

from django.db import models
from django.db.models.fields import PositiveSmallIntegerField
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.contrib.sessions.models import Session
from django.core.files import File

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Goods(models.Model):
	code = models.CharField(max_length=30, unique=True)
	articul = models.CharField(max_length=30)
	producer = models.ForeignKey('Producers')
	description = models.TextField()
	category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
	in_stock = models.IntegerField(default=0, null=True, blank=True)
	price = models.FloatField(null=True, blank=True)
	price_2 = models.FloatField(null=True, blank=True)
	price_3 = models.FloatField(null=True, blank=True)	
	price_5 = models.FloatField(null=True, blank=True)
	price_6 = models.FloatField(null=True, blank=True)
	price_7 = models.FloatField(null=True, blank=True)
	price_8 = models.FloatField(null=True, blank=True)
	price_9 = models.FloatField(null=True, blank=True)
	price_10 = models.FloatField(null=True, blank=True)
	price_11 = models.FloatField(null=True, blank=True)
	price_12 = models.FloatField(null=True, blank=True)
	price_13 = models.FloatField(null=True, blank=True)
	price_14 = models.FloatField(null=True, blank=True)
	price_15 = models.FloatField(null=True, blank=True)
	price_16 = models.FloatField(null=True, blank=True)
	price_17 = models.FloatField(null=True, blank=True)
	price_18 = models.FloatField(null=True, blank=True)
	price_19 = models.FloatField(null=True, blank=True)
	price_20 = models.FloatField(null=True, blank=True)
	photo = models.ForeignKey('Photo', blank=True, null=True, on_delete=models.SET_NULL)
	order_count = models.PositiveSmallIntegerField(blank=True, null=True)
	
	def get_in_stock(self):
		if in_stock:
			return '+'
		else:
			return ''






	def __str__(self):
		return "{}".format(self.code)

	class Meta:
		unique_together = ('code', 'articul')
		verbose_name = 'Товар'
		verbose_name_plural = 'Товары'
		ordering = ['code']




class Category(models.Model):
	name = models.CharField(max_length=30)
	description = models.TextField(null=True)

	def __str__(self):
		return self.name


	class Meta:
		verbose_name = 'Категория'
		verbose_name_plural = 'Категории'



class Photo(models.Model):
	name = models.CharField(max_length=50)
	description = models.TextField(null=True)
	date = models.DateTimeField(auto_now=True)	
	photo_width = models.IntegerField(default=0)
	photo_height = models.IntegerField(default=0)
	photo = models.ImageField(null=True, blank=True)
	code = models.IntegerField()
	image_url = models.URLField(null=True, blank=True)


	def get_remote_image(self, path):
		if self.image_url and not self.photo:
			result = urllib.request.urlretrieve(self.image_url)
			print('result', result)
			self.photo.save('.' + path + self.name + self.image_url.rsplit('.')[-1], File(open(result[0], 'rb')))
			#self.photo.save(os.path.basename(self.name + self.image_url.rsplit('.')[-1]), File(open(result[0], 'rb')))
			self.save()



	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('index:detail', kwargs={'id': self.id})

	def change_size_img(self):
		#Opening the uploaded image
		im = Image.open(self.photo)

		output = BytesIO()

		#Resize/modify the image
		im = im.resize((self.photo_width, self.photo_height))

		#after modifications, save it to the output
		im.save(output, format='PNG', quality=100)
		output.seek(0)

		#change the imagefield value to be the newley modifed image value
		self.photo = InMemoryUploadedFile(output,'ImageField', "%s.png" %self.photo.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)


	class Meta:
		ordering = ['date']
		verbose_name = 'Изображение'
		verbose_name_plural = 'Изображения'


class UploadsImage(models.Model):
	img_width = PositiveSmallIntegerField()
	img_height = PositiveSmallIntegerField()
	image = models.ImageField(upload_to = "goods/image", width_field = 'img_width', height_field = 'img_height')

	class Meta:
		verbose_name = 'Загрузки'
		verbose_name_plural = 'Загрузки'

class FileUpload(models.Model):
	name = models.CharField(max_length=50, default='SOME STRING')
	file = models.FileField(upload_to = "goods/file")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Файл'
		verbose_name_plural = 'Файлы'




class Producers(models.Model):
	name = models.CharField(max_length=50)
	description = models.TextField(null=True, blank=True)
	photo = models.ForeignKey(Photo, blank=True, null=True)
	rating = models.IntegerField(null=True, blank=True, verbose_name='рейтинг')
	visibility = models.BooleanField(default=False, db_index=True, verbose_name='отображать')


	def __str__(self):
		return "{}, рейтинг:{}, отобржать: {}".format(self.name, self.rating, self.visibility)

	class Meta:
		verbose_name = 'Производитель'
		verbose_name_plural = 'Производители'




class NewGoods(models.Model):
	position = models.ForeignKey(Goods, null=True, blank=True,)
	date = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.position.code


	class Meta:
		verbose_name = 'Новинка'
		verbose_name_plural = 'Новинки'	


