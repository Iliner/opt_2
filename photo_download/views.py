import os

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.files import File
from django.core.files.images import ImageFile

from main_page.models import Goods
from main_page.models import Photo


from bs4 import BeautifulSoup
import requests
import urllib.request
import urllib3
import re
import csv
import subprocess
from addons.excel_views import Excel

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')


@csrf_exempt
def download_photo_view(request):
	goods = Goods.objects.filter(photo=None)
	for_stock_excel = {}
	#goods = goods.filter(producer__name='Forsage')	
	count = 0
	for good in goods:
		distribution_function(good.producer.name, good.code, good.articul)
		url_photo = parser_th_tools(good.code)
		if url_photo and count < 3:
			new_photo = Photo()
			new_photo.name = good.code
			new_photo.image_url = url_photo
			new_photo.code = good.code
			new_photo.save()
			new_photo.get_remote_image('/goods/photos/')
			good.photo = new_photo
			good.save()
			for_stock_excel.update({good.code: good.photo.photo.url})
			count += 1
			#full_name = dowanload_on_server(url_photo, good.code)
			# if full_name:
			# 	full_path = "{}/goods/photos/{}".format(MEDIA_ROOT, full_name)
			# 	new_photo = Photo()
			# 	new_photo.name = good.code
			# 	new_photo.photo = ImageFile(open(full_path, "rb"))
			# 	new_photo.code = good.code
			# 	new_photo.save()
			# 	new_photo.photo.url('media/goods/photos/' + full_name)
			# 	new_photo.save()
			# 	good.photo = new_photo
			# 	good.save()

	excel_stock(for_stock_excel)
	return HttpResponse(goods)


def excel_stock(_dict):
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	full_path = "{}/uploads/{}".format(BASE_DIR, 'stock.xlsx')
	meta = {"code": 0, 'photo': 12}
	print(_dict)
	ex = Excel(
		full_path,
		meta,
		)








def distribution_function(producer, code, articul):
	result = None
	dict_with_brands = {
		'h-d.by': ['CYNEL', 'FLO','GAV','GEKO','GERLACH','H-D','JUCO','LUND','LUXI','NORMA','POWER UP','POWERUP','PROWIN',
		     'STHOR','TOYA','VOREL','YATO','Zeta','ZMM MAXPOL','Сибиар',],
		'tools.by': ['Строительный Инструмент', 'Fermer', 'Eco', 'Startul', 'Toptul', 'Wortex', 'Solaris', 'Oleo-Mac', 'Fiskars', 
		     'Gepard', 'Юпитер', 'Starfix', 'ВОЛАТ', 'Sola', 'Wilo', 'Telwin', 'Slowik', 'Molot'],
		'th-tool.by': ['Авто Инструмент', 'BaumAuto', 'Big Red', 'BRAUMAUTO', 'D&D', 'FORCEKRAFT', 'Forsage', 'Forsage electro', 
		     'FORSAGE kids', 'HCB', 'JTC', 'KINGTUL', 'KingTul kraft', 'KINGTUL profi', 'KINGTUL(SK)', 'M7', 'MARSHAL', 'Partner', 'Prowin', 'Rotake']
	}
	
	for store, list_producer in dict_with_brands.items():
		for store_producer in list_producer:
			store_producer = store_producer.lower().strip().replace(' ', '')
			producer = producer.lower().strip().replace(' ', '')
			if producer == store_producer:
				if store == 'h-d.by':
					result = parser_h_d(articul)
				elif store == 'tools.by':
					result = parser_tools(articul)
				elif store == 'th-tool.by':	
					result = parser_th_tools(code)
				break
	return result




def parser_th_tools(code):
	href_photo = None 
	url = requests.get('http://th-tool.by/index.php?route=product/search&search=' + code)
	soup = BeautifulSoup(url.text, 'html.parser')
	searcher = soup.find_all('a') 
	for i in searcher:
		if(i.get('href')):
			var = i.get('href').find(code)
			if(var >= 0):
				url = requests.get(i.get('href'))
				soup = BeautifulSoup(url.text, 'html.parser')
				try:
					div = soup.find('div', {'class': 'image'}).next
					href_photo = div.get('href')
				except AttributeError as err:
				  	continue
	return href_photo


def parser_tools(articul):
	url = requests.get('http://www.tools.by/?q=kat&part=1&keys=' + articul) # Страница с которого мы будем парсить в конце меняем на нужный нам код
	soup = BeautifulSoup(url.text, 'html.parser')
	try:
		searcher = soup.find('tr', class_='subtitle odd').next_sibling.next_sibling
		searcher = searcher.find('td')
		find_need_data = searcher.find('a', class_='zzoom')
		find_need_data = find_need_data.get('big')
		link = 'http://www.tools.by' + find_need_data
		url = requests.get(link)
		soup = BeautifulSoup(url.text, 'html.parser')
		else_searcher = soup.find('img')
		else_searcher = else_searcher.get('src')
		href_photo = 'http://www.tools.by' + else_searcher
	except AttributeError as err:
		print('Произошла ошибка или нет такого товара вообще: ' + articul)
		href_photo = None
	return href_photo




def parser_h_d(articul):
	url = requests.get('http://h-d.by/buscar?orderby=position&orderway=desc&search_query={}&submit_search='.format(articul)) # Страница с которого мы будем парсить в конце меняем на нужный нам код
	soup = BeautifulSoup(url.text, 'html.parser')
	try:
		searcher = soup.find('div', class_='center_block')
		searcher = searcher.find('a', class_='product_img_link')
		href_for_big_photo = searcher.get('href')
		url = requests.get(href_for_big_photo)
		soup = BeautifulSoup(url.text, 'html.parser')
		searcher = soup.find('div', class_='image-block').find('img')
		href_photo = searcher.get('src')
	except AttributeError as err:
		print('Произошла ошибка или нет такого товара вообще: ' + articul)
		href_photo = None
	return href_photo





def dowanload_on_server(link, code):
	dir_path_photo = BASE_DIR + '/uploads/goods/photos/'
	url = link
	get_photo = requests.get(url)
	format_photo = url.rsplit('.', maxsplit=1)[-1]
	full_name = "{}.{}".format(code, format_photo)
	full_path = dir_path_photo + full_name
	try:         
		file = open(full_path, 'wb')
		file.write(get_photo.content)
		file.close()
	except FileNotFoundError as err:
		print(err)
		full_name = None
	return full_name












#   def download(self, path):
#     if self.dict_for_download:
#       for link, data in self.dict_for_download.items():
#         url = link
#         print('download', link, data)
#         get_photo = requests.get(link)
#         format_photo = url.rsplit('.', maxsplit=1)[-1]
#         full_name = data[0] + "." + format_photo
#         try:
#          file = open(path + full_name, 'wb')
#          file.write(get_photo.content)
#          file.close()
#         except FileNotFoundError as err:
#          print(err)
#       self.clear_dict_for_download()


#   def dowanload_on_server(self):
#     """
#     Функция непосредственно скачивает фото на сервере
#     """
#     if self.dict_for_download:
#       for link, data in self.dict_for_download.items():
#         url = link
#         get_photo = requests.get(url)
#         format_photo = url.rsplit('.', maxsplit=1)[-1]
#         full_name = data[0] + "." + format_photo
#         #producer_1 = producer.capitalize()
#         """
#         Меняем имена так как они указаны с учетом из название в репозитории 
#         """
#         producer = self.__change_producer_like_server(data[1])
#         producer_2 = producer.lower()
#         producer_2 = producer_2.replace(' ', '')
#         #print(producer_2 + '_bot' '/' + full_name)
#         try:         
#           file = open('/var/www/opt-online/photos/bot_producer/' + producer_2 + '_bot' '/' + full_name, 'wb')
#           file.write(get_photo.content)
#           file.close()
#           print(producer_2 + '_bot' '/' + full_name)    
#           self.crop_for_page(producer_2, full_name)
#           self.crop_for_search(producer_2, full_name)
#         except FileNotFoundError as err:
#           print(err)
#       self.clear_dict_for_download()











#   def __change_producer_like_server(self, producer):       
#        if producer == 'D&D' or producer == 'd&d':
#               producer = 'dandd'
#        elif producer == 'Юпитер':
#               producer = 'jupiter'
#        elif producer == 'Белстаб':
#               producer = 'belstub'
#        elif producer == 'KingTul kraft':
#               producer = 'kingtulkraft'
#        elif producer == 'big red':
#               producer = 'bigred'
#        elif producer == 'KINGTUL profi':
#               producer = 'kingtulprofi'
#        elif producer == 'ПрофКлей':
#               producer = 'profcley'
#        elif producer == 'HÖGERT technik':
#               producer = 'hogert'
#        elif producer == 'ПрофКлей':
#               producer = 'profcley' 

#        return producer

  


# if __name__ == '__main__':
#   print('\nРабота старта началась\n')
#   dict_with_brands = {
#   'h-d.by': ['CYNEL', 'FLO','GAV','GEKO','GERLACH','H-D','JUCO','LUND','LUXI','NORMA','POWER UP','POWERUP','PROWIN',
#          'STHOR','TOYA','VOREL','YATO','Zeta','ZMM MAXPOL','Сибиар',],
#   'tools.by': ['Строительный Инструмент', 'Fermer', 'Eco', 'Startul', 'Toptul', 'Wortex', 'Solaris', 'Oleo-Mac', 'Fiskars', 
#          'Gepard', 'Юпитер', 'Starfix', 'ВОЛАТ', 'Sola', 'Wilo', 'Telwin', 'Slowik', 'Molot'],
#   'th-tool.by': ['Авто Инструмент', 'BaumAuto', 'Big Red', 'BRAUMAUTO', 'D&D', 'FORCEKRAFT', 'Forsage', 'Forsage electro', 
#          'FORSAGE kids', 'HCB', 'JTC', 'KINGTUL', 'KingTul kraft', 'KINGTUL profi', 'KINGTUL(SK)', 'M7', 'MARSHAL', 'Partner', 'Prowin', 'Rotake']
#   }

#   #csv_path = "/var/www/opt-online/dataXlsx/opt_new/opt_clear.csv"
#   csv_path = "/var/www/opt-online/dataXlsx/havenot.csv"
#   first = ParserCore(csv_path, field_code=0, field_producer=1, field_article=2)
#   first.add_dict_with_brand(dict_with_brands) 
  



#   first.parser_th_tools()
#   #print(first.dict_for_download)
#   first.parser_tools()
#   #print(first.dict_for_download)
#   first.parser_h_d()
#   first.dowanload_on_server()










  # def parser_tools(self, dict=''):
  #   """По артиклу
  #   """
  #   if self.dicts_data:
  #     my_dict =  self.dicts_data['tools.by']
  #     l = 0
  #     dict_with_url = {}
  #     for code, value in my_dict.items():
  #       l += 1
  #       if l < 10:
  #         print(value[0])
  #         url = requests.get('http://www.tools.by/?q=kat&part=1&keys=' + value[0]) # Страница с которого мы будем парсить в конце меняем на нужный нам код
  #         soup = BeautifulSoup(url.text, 'html.parser')
  #         try:
  #           searcher = soup.find('tr', class_='subtitle odd').next_sibling.next_sibling
  #           searcher = searcher.find('td')
  #           find_need_data = searcher.find('a', class_='zzoom')
  #           find_need_data = find_need_data.get('big')
  #           link = 'http://www.tools.by' + find_need_data
  #           url = requests.get(link)
  #           soup = BeautifulSoup(url.text, 'html.parser')
  #           else_searcher = soup.find('img')
  #           else_searcher = else_searcher.get('src')
  #           href_photo = 'http://www.tools.by' + else_searcher
  #         except AttributeError as err:
  #           print('Произошла ошибка или нет такого товара вообще: ' + value[0])
  #           continue
  #         else:
  #           dict_with_url[href_photo] = (code, value[1])
  #     self.__dict_download_plus_url(dict_with_url)
  #     return dict_with_url



  # def parser_h_d(self, dict=''):
  #   """Ищем по артиклу
  #   """ 

  #   if self.dicts_data:
  #     my_dict =  self.dicts_data['h-d.by']
  #     l = 0
  #     dict_with_url = {}
  #     for code, value in my_dict.items():
  #       l += 1
  #       if l < 10:
  #         url = requests.get('http://h-d.by/buscar?orderby=position&orderway=desc&search_query={}&submit_search='.format(value[0])) # Страница с которого мы будем парсить в конце меняем на нужный нам код
  #         soup = BeautifulSoup(url.text, 'html.parser')
  #         try:
  #           searcher = soup.find('div', class_='center_block')
  #           searcher = searcher.find('a', class_='product_img_link')
  #           href_for_big_photo = searcher.get('href')
  #           url = requests.get(href_for_big_photo)
  #           soup = BeautifulSoup(url.text, 'html.parser')
  #           searcher = soup.find('div', class_='image-block').find('img')
  #           href_photo = searcher.get('src')
  #         except AttributeError as err:
  #           print('Произошла ошибка или нет такого товара вообще: ' + value[0])
  #           continue
  #         else:
  #           dict_with_url[href_photo] = (code, value[1])
  #     self.__dict_download_plus_url(dict_with_url)
  #     return dict_with_url
