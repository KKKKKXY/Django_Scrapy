from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from scrapy_thai_app.thai_spider.thai_spider.multi_run_thai import *
from scrapy_eng_app.eng_spider.eng_spider.multi_run_eng import *
from rest_framework import routers
from file_manage_app.views import *

router = routers.DefaultRouter()
router.register(r'upload_file', FileUploadViewSet)
router.register(r'all_files', FileViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('send_thai_captcha_email/', getThaiCaptchaEmail),
    path('send_eng_captcha_email/', getEngCaptchaEmail),
    path('run_thai_spider/', run_thai_spider),
    path('run_eng_spider/', run_eng_spider),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
