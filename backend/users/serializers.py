from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UploadedFile,Summary


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['id', 'user', 'file', 'file_name', 'uploaded_at']
        extra_kwargs = {
            'user': {'read_only': True},  
            'file_name': {'required': False}  
        }

    def create(self, validated_data):
        validated_data['file_name'] = validated_data['file'].name  
        return super().create(validated_data)
    
class SummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Summary
        fields = '__all__'


class QuestionAnswerSerializer(serializers.Serializer):
    summary_id = serializers.IntegerField()
    question = serializers.CharField(max_length=500)
    answer = serializers.CharField(read_only=True)