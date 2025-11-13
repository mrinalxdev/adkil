from django.urls import path
from . import views

urlpatterns = [
    path('', views.AudioUploadView.as_view(), name='upload-audio'),
]