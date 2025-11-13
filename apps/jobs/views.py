from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_rq import enqueue
from .models import ProcessingJob
from .serializers import ProcessingJobSerializer, CreateJobSerializer
from .tasks import process_job

class JobCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CreateJobSerializer(data=request.data)
        if serializer.is_valid():
            audio_file_id = serializer.validated_data['audio_file_id']
            job_type = serializer.validated_data['job_type']
            
            job = ProcessingJob.objects.create(
                audio_file_id=audio_file_id,
                job_type=job_type
            )
            enqueue(process_job, job.id, job_timeout=-1)
            return Response(ProcessingJobSerializer(job).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JobDetailView(APIView):
    def get(self, request, pk, *args, **kwargs):
        job = get_object_or_404(ProcessingJob, pk=pk)
        serializer = ProcessingJobSerializer(job)
        return Response(serializer.data)