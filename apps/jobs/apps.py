from django.apps import AppConfig
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import django_rq

class JobsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.jobs'
    
    def ready(self):
        if settings.DEBUG:
            return
            
        scheduler = django_rq.get_scheduler('default')
        
       
        scheduler.schedule(
            scheduled_time=timezone.now(),
            func='apps.jobs.tasks.cleanup_old_artifacts',
            interval=60 * 60 * 24, 
            repeat=None  
        )