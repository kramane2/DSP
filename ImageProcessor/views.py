import os
import time
from wsgiref.util import FileWrapper

import cv2
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse, JsonResponse
from rest_framework import generics

from ImageProcessor.models import ProcessedImageModel
from ImageProcessor.serializer import RawImageSerializer, ProcessedImageSerializer


class ImageUploadView(generics.ListAPIView):
    serializer_class = RawImageSerializer

    def get_queryset(self):
        return

    def post(self, request, *args, **kwargs):
        for file in request.FILES.getlist("floor_plan"):
            save_image_to_folder('tmp/', file)
        return HttpResponse(status=200)


def save_image_to_folder(folder, file):
    default_storage.save(folder + file.name, ContentFile(file.read()))


def load_first_n_images_from_folder(number_of_images, folder):
    images = []
    for filename in os.listdir(folder)[:number_of_images]:
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(ProcessedImageModel(img, 7, 7, 7, 7))
    return images


class ResultsView(generics.ListAPIView):
    # Trigger processing
    # Processing 2.5 seconds
    time.sleep(2.5)

    serializer_class = ProcessedImageSerializer

    def get_queryset(self):
        return

    def get(self, request, *args, **kwargs):
        # TODO: hardcoded data
        data = [{
            "floor_plan": "8_multi.png",
            "area": 66,
            "compartments": 66,
            "windows": 66,
            "doors": 66
        },
            {
                "floor_plan": "9_multi.png",
                "area": 55,
                "compartments": 55,
                "windows": 55,
                "doors": 55
            }
        ]

        return JsonResponse(data, safe=False, status=200)


class CsvView(generics.CreateAPIView):
    def get(self, request, *args, **kwargs):  # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

        document = open("processed/test.csv", 'rb')
        response = HttpResponse(FileWrapper(document), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="test.csv"'
        return response
