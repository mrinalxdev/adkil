from django.db import models

from django.db.models import Manager
from apps.uploads.models import AudioFile

# Define choices at module level (optional but clean)
JOB_TYPES = [
    ('extract-metadata', 'Extract Metadata'),
    ('convert-to-wav', 'Convert to WAV'),
]

class ProcessingJob(models.Model):
    
    objects : Manager["ProcessingJob"]
    
    audio_file = models.ForeignKey(AudioFile, on_delete=models.CASCADE)
    job_type = models.CharField(max_length=50, choices=JOB_TYPES)
    status = models.CharField(
        max_length=20,
        default='queued',
        choices=[
            ('queued', 'Queued'),
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('failed', 'Failed')
        ]
    )
    result = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.job_type} - {self.status}"