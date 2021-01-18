import base64
import os
import time
from wsgiref.util import FileWrapper

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import generics

from API.compartment_counter import get_floor_plan_compartments
from API.in_mem_floor_plans import InMemFloorPlans
from API.models import FloorPlansCsvData
from API.serializer import RawImageSerializer
from floor_plan_model.display import init_model, process_img

path_weights = 'floor_plan_model/models/Jan12/G'
model = init_model(path_weights=path_weights)
floor_plan_in_mem_db = InMemFloorPlans()


class ImageUploadView(generics.ListAPIView):
    serializer_class = RawImageSerializer

    def get_queryset(self):
        return

    def post(self, request, *args, **kwargs):
        floor_plan_in_mem_db.floor_plan_names = []
        for file in request.FILES.getlist("floor_plan"):
            floor_plan_in_mem_db.floor_plan_names.append(file.name)
            save_image_to_folder('tmp/', file)
        return HttpResponse(status=200)


def save_image_to_folder(folder, file):
    default_storage.save(folder + file.name, ContentFile(file.read()))


def convert_image_to_base64(img_name):
    with open(img_name, "rb") as img_file:
        return base64.b64encode(img_file.read())


def get_floor_plan_data_json(file_name, compartments):
    os.remove("tmp/" + file_name)
    org_name = "original_" + file_name
    original_floor_plan_1 = convert_image_to_base64("tmp/" + org_name)
    proc_name = "processed_" + file_name
    processed_floor_plan_1 = convert_image_to_base64("tmp/" + proc_name)
    os.remove("tmp/" + org_name)
    os.remove("tmp/" + proc_name)
    return {
        "original_floor_plan_name": org_name,
        "original_floor_plan_image": original_floor_plan_1.decode(),
        "processed_floor_plan_name": proc_name,
        "processed_floor_plan_image": processed_floor_plan_1.decode(),
        "living_room": compartments.living_room,
        "hall": compartments.hall,
        "bathroom": compartments.bathroom,
        "bedroom": compartments.bedroom,
        "closet": compartments.closet,
        "door": compartments.door
    }


class ResultsView(generics.ListAPIView):
    # Trigger processing
    # Processing 2.5 seconds
    time.sleep(2.5)

    def get_queryset(self):
        return

    def get(self, request, *args, **kwargs):
        floor_plans_json_data = []
        floor_plans_csv_data = FloorPlansCsvData()
        for file_name in floor_plan_in_mem_db.floor_plan_names:
            compartments = get_floor_plan_compartments(process_img(file_name, model))
            floor_plans_json_data.append(get_floor_plan_data_json(file_name, compartments))
            floor_plans_csv_data.append_special(file_name, compartments.closet, compartments.bathroom,
                                                compartments.living_room, compartments.bedroom, compartments.hall,
                                                compartments.door)
        floor_plans_csv_data.to_csv()
        return JsonResponse(floor_plans_json_data, safe=False, status=200)


class CsvView(generics.CreateAPIView):
    def get(self, request, *args, **kwargs):  # Create the HttpResponse object with the appropriate CSV header.
        document = open("tmp/data.csv", 'rb')
        response = HttpResponse(FileWrapper(document), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="data.csv"'
        return response


def index(request):
    # Render the HTML template index.html
    return render(request, "index.html")
