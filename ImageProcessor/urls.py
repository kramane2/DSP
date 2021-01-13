"""ImageProcessor URL Configuration

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
from django.urls import path

from ImageProcessor.views import ImageUploadView, ResultsView, CsvView

urlpatterns = [
    # POST
    # Input: list of images
    # Returns OK
    path('images/upload', ImageUploadView.as_view(), name='image-list'),
    # GET
    # Should return list of ImageProcessor.ProcessedImageModel
    path('images/process', ResultsView.as_view()),
    # GET
    # Returns CSV file
    path('images/results', CsvView.as_view()),
    path('test', CsvView.as_view())
]