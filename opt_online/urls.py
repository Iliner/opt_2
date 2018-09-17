"""opt_online URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', login,  {'template_name': 'registration/login.html'}, name="login"),
    url(r'^logout/', logout, {'template_name': 'registration/logout.html'}, name="logout"),
    url(r'', include('main_page.urls')),
    url(r'', include('basket.urls')),
    url(r'', include('imagepool.urls'))
       
]


urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) 

# if settings.DEBUG:
# 	urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
# 	urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) 