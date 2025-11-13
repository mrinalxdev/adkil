from rest_framework import serializers
from .models import ProcessingJob, JOB_TYPES

class ProcessingJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessingJob
        fields = ['id', 'audio_file', 'job_type', 'status', 'result', 'created_at']

class CreateJobSerializer(serializers.Serializer):
    audio_file_id = serializers.IntegerField()
    job_type = serializers.ChoiceField(choices=[choice[0] for choice in JOB_TYPES])