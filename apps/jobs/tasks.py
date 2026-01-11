import shutil
from datetime import timedelta
from django.utils import timezone
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
        
    
def cleanup_old_artifacts():
    try:
        ttl_hours = 24
        cutoff_time = timezone.now() - timedelta(hours=ttl_hours)
        
        
        old_jobs = ProcessingJob.objects.filter(
            status_in=['completed', 'failed'],
            updated_at_lt=cutoff_time
        )
        
        deleted_count = 0
        for job in old_jobs:
            try :
                audio_file = job.audio_file
                if audio_file.file and os.path.exists(audio_file.file.path):
                    os.remove(audio_file.file.path)
                    #we will be also looking for any related artificats
                    #but 
                    artifact_dir = os.path.join(settings.MEDIA_ROOT, 'artificats', str(job.id))
                    
                    if os.path.exists(artifact_dir) :
                        shutil.rmtree(artifact_dir)
                        
                
                audio_file.delete()
                job.delete()
                deleted_count += 1
        
    
            except Exception as e:
                print(f"Error deleting artificats for job {job.id} : {str(e)}")
                continue
        
        
        audio_dir = os.path.join(settings.MEDIA_ROOT, 'audio')
        if os.path.exists(audio_dir):
            for filename in os.listdir(audio_dir):
                file_path = os.path.join(audio_dir, filename)
                
                try :
                    if os.path.getmtime(file_path) < cutoff_time.timestamp():
                        os.remove(file_path)
                        deleted_count += 1
                
                except Exception as e:
                    print(f"Error deleting orphaned file {filename} : {str(e)}")
    
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
        