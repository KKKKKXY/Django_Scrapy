from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from scrapy_thai_app.profile_models import DBDCompany_Thai
from scrapy_thai_app.serializers import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets

# Create your views here.
@csrf_exempt
def get_data(request):
	data = DBDCompany_Thai.objects.all()
	if request.method == 'GET':
		serializer = CompanyThaiSerializer(data, many=True)
		return JsonResponse(serializer.data, safe=False)

class CompanyThaiViewSet(viewsets.ModelViewSet):
    queryset = DBDCompany_Thai.objects.all()
    serializer_class = CompanyThaiSerializer
