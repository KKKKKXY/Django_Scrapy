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

from scrapy_thai_app.views import *
from scrapy_thai_app.multi_run_thai import runspider
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'companies_thai', CompanyThaiViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('getData/', get_data),
    path('', include(router.urls)),
    path('run_thai_spider/', runspider),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
