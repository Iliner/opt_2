from django.db import models
from django.db.models.fields import PositiveSmallIntegerField
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.contrib.sessions.models import Session


class Goods(models.Model):
	code = models.CharField(max_length=30, unique=True)
	articul = models.CharField(max_length=30)
	producer = models.ForeignKey('Producers')
	description = models.TextField()
	category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
	in_stock = models.CharField(max_length=20, null=True)
	price = models.FloatField()
	price_2 = models.FloatField(null=True, blank=True)
	price_3 = models.FloatField(null=True, blank=True)	
	price_5 = models.FloatField(null=True, blank=True)
	price_6 = models.FloatField(null=True, blank=True)
	photo = models.ForeignKey('Photo', blank=True, null=True)
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
	photo = models.ImageField()
	code = models.IntegerField()

	image_url = models.URLField(null=True, blank=True)


	def get_remote_image(self):
		if self.image_url and not self.photo:
			result = urllib.urlretrieve(self.image_url)
			self.photo.save(os.path.basename(self.name + self.image_url.rsplit('.')[-1]), File(open(result[0])))
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

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Производитель'
		verbose_name_plural = 'Производители'



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


class NewGoods(models.Model):
	position = models.ForeignKey(Goods, null=True, blank=True,)
	date = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.position.code


	class Meta:
		verbose_name = 'Новинка'
		verbose_name_plural = 'Новинки'	


class BannerStock(models.Model):
	name = models.CharField(max_length=50, blank=True, null=True)
	date =  models.DateTimeField(auto_now=True, editable=True,)
	img =  models.ImageField(upload_to = "banner/")


	def __str__(self):
		return self.name


	class Meta:
		verbose_name = 'Баннер_акций'
		verbose_name_plural = 'Баннеры_акций'	
