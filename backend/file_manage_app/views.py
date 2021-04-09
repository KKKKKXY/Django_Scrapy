# import needed lib
from django.shortcuts import render
from rest_framework import status
from .serializers import FileSerializer
from django.http import HttpResponse
from rest_framework import viewsets
# import own lib
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