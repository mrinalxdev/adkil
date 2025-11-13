from rest_framework import serializers
from .models import AudioFile

class AudioFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioFile
        fields = ['id', 'file', 'uploaded_at']