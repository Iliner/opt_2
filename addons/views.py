from io import BytesIO
import os
from django.shortcuts import render
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.base import ContextMixin
from django.views.generic.base import TemplateView
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .models import *
from xhtml2pdf import pisa
from basket.models import Manager

class BannerView(ListView):
	template_name = 'addons/banner.html'
	paginate_by = 100
	customer = None
	manager = None

	def get(self, request, *args, **kwargs):

		if request.user.is_authenticated():
			try:
				self.customer = request.user.customer_set.first()
				self.opt_user = request.user.customer_set.first().opt
			except Exception as err:
				print(err)
		else:
			return redirect('login')



		try:
			self.manager = Manager.objects.get(customers=self.customer)
		except Exception as err:
			print(err)	
		
		return super(BannerView, self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(BannerView, self).get_context_data(**kwargs)

		if self.manager:
			context['manager_first_name'] = self.manager.first_name
			context['manager_last_name'] = self.manager.last_name
			context['manager_mail_work'] = self.manager.mail_work
			context['manager_phone_number_work'] = self.manager.phone_number_work

		return context



	def get_queryset(self): 
		return BannerStock.objects.filter(visibility=True).order_by('-date')




class CatalogImgView(ListView):
	template_name = 'addons/catalog_pdf.html'
	customer = None
	manager = None

	def get(self, request, *args, **kwargs):

		if request.user.is_authenticated():
			try:
				self.customer = request.user.customer_set.first()
			except Exception as err:
				print(err)
		else:
			return redirect('login')


		try:
			self.manager = Manager.objects.get(customers=self.customer)
		except Exception as err:
			print(err)	
		
		return super(CatalogImgView, self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(CatalogImgView, self).get_context_data(**kwargs)

		if self.manager:
			context['manager_first_name'] = self.manager.first_name
			context['manager_last_name'] = self.manager.last_name
			context['manager_mail_work'] = self.manager.mail_work
			context['manager_phone_number_work'] = self.manager.phone_number_work

		return context

	def get_queryset(self): 
		return PdfCatalogs.objects.all().order_by('-date')












def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None








class CatalogOpenView(View):
	def get(self, request, *args, **kwargs):
		catalog_id = self.kwargs['catalog_id']
		need_catalog = PdfCatalogs.objects.get(id=catalog_id)
		#/home/ivan/Документы/local/python/mydjango/opt_online/uploads/pdf/pdf_catalog
		base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		with open(base_dir + '/uploads/' + str(need_catalog.file), 'rb') as pdf:
			response = HttpResponse(pdf.read(), content_type='application/pdf')
			response['Content-Disposition'] = 'inline;filename=some_file.pdf'
			return response
		pdf.closed
		



	# def get(self, request, *args, **kwargs):
 #         template = get_template('addons/catalog_open.html')
 #         catalog_id = self.kwargs['catalog_id']
 #         need_catalog = PdfCatalogs.objects.get(id=catalog_id)
 #         print(need_catalog.file)
 #         context = {
 #         	'path': need_catalog.file
 #         }
 #         html = template.render(context)
 #         pdf = render_to_pdf('addons/catalog_open.html', context)
 #         if pdf:
 #             response = HttpResponse(pdf, content_type='application/pdf')
 #             filename = "Invoice_%s.pdf" %("12341231")
 #             content = "inline; filename='%s'" %(filename)
 #             download = request.GET.get("download")
 #             if download:
 #                 content = "attachment; filename='%s'" %(filename)
 #             response['Content-Disposition'] = content
 #             return response
 #         return HttpResponse("Not found")	




# class CatalogPdfView(View):
#      def get(self, request, *args, **kwargs):
#          template = get_template('invoice.html')
#          context = {
#              "invoice_id": 123,
#              "customer_name": "John Cooper",
#              "amount": 1399.99,
#              "today": "Today",
#          }
#          html = template.render(context)
#          pdf = render_to_pdf('invoice.html', context)
#          if pdf:
#              response = HttpResponse(pdf, content_type='application/pdf')
#              filename = "Invoice_%s.pdf" %("12341231")
#              content = "inline; filename='%s'" %(filename)
#              download = request.GET.get("download")
#              if download:
#                  content = "attachment; filename='%s'" %(filename)
#              response['Content-Disposition'] = content
#              return response
#          return HttpResponse("Not found")


@csrf_exempt
def hidden_opt(request):
	opt_status = request.session.get('opt_status')
	if opt_status == 'hidden':
		request.session['opt_status'] = None
	else:
		request.session['opt_status'] = 'hidden'
	
	return HttpResponse(request.POST.get('url'))