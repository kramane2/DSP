from rest_framework import serializers
from ImageProcessor.models import RawImageModel, ProcessedImageModel


class RawImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawImageModel
        fields = '__all__'


class ProcessedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessedImageModel
        fields = '__all__'