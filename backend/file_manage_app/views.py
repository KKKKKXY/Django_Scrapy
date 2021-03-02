from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import FileSerializer
from django.views.decorators.csrf import csrf_exempt
import json
import base64
from django.http import HttpResponse
from rest_framework import viewsets
from .models import File

# Create your views here.
class FileUploadViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def post(self, request, *args, **kwargs):
        filename    = request.data['filename']
        file        = request.data['file']
        file_type   = request.data['file_type']
        File.objects.create(filename=filename, file=file, file_type=file_type)
        return HttpResponse({'message': 'File uploaded'}, status=200)

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer