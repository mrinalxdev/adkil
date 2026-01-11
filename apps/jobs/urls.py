from django.urls import path
from . import views

urlpatterns = [
    path('', views.JobCreateView.as_view(), name='create-job'),
    path('<int:pk>/', views.JobDetailView.as_view(), name='job-detail'),
    path('cleanup/', views.CleanupArtifactsView.as_view(), name='cleanup-artifacts')
]