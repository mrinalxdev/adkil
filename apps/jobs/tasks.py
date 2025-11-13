import os
from mutagen import File as MutagenFile
from django.conf import settings
from .models import ProcessingJob

def process_job(job_id):
    job = ProcessingJob.objects.get(id=job_id)
    job.status = 'processing'
    job.save(update_fields=['status'])
    
    

    try:
        audio_path = job.audio_file.file.path
        if job.job_type == 'extract-metadata':
            metadata = extract_audio_metadata(audio_path)
            job.result = metadata
        elif job.job_type == 'convert-to-wav':
            job.result = {"message": "WAV conversion not implemented in minimal version"}
        else:
            raise ValueError(f"Unknown job type: {job.job_type}")
        
        job.status = 'completed'
    except Exception as e:
        job.status = 'failed'
        job.result = {"error": str(e)}
    
    job.save(update_fields=['status', 'result'])

def extract_audio_metadata(file_path):
    try:
        audio = MutagenFile(file_path)
        if audio is None:
            return {"error": "Unsupported file format"}
        
        metadata = {}
        for key, value in audio.items():
            if isinstance(value, list):
                metadata[key] = str(value[0]) if value else ""
            else:
                metadata[key] = str(value)
        return metadata
    except Exception as e:
        return {"error": str(e)}