"""base URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from scrapy_thai_app.views import *
from scrapy_thai_app.thai_spider.thai_spider.multi_run_thai import *
from scrapy_eng_app.eng_spider.eng_spider.multi_run_eng import *
from rest_framework import routers
from file_manage_app.views import *

router = routers.DefaultRouter()
router.register(r'companies_thai', CompanyThaiViewSet)
router.register(r'upload_file', FileUploadViewSet)
router.register(r'all_files', FileViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('getData/', get_data),
    path('', include(router.urls)),
    path('send_thai_captcha_email/', getThaiCaptchaEmail),
    path('send_eng_captcha_email/', getEngCaptchaEmail),
    path('run_thai_spider/', run_thai_spider),
    path('run_eng_spider/', run_eng_spider),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
