from django.urls import path
from rest_framework import permissions
from .views import *
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger Schema View
schema_view = get_schema_view(
   openapi.Info(
      title="Kid & Doctor API",
      default_version='v1',
      description="API for managing doctors, kids, media, and voice recordings.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@yourapi.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),  # Disable auth for the Swagger view

)

urlpatterns = [
    # Swagger URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    # Doctor Registration
    path('doctor/register/', DoctorCreateView.as_view(), name='doctor-register'),

    # Doctor Login
    path('doctor/login/', DoctorLoginView.as_view(), name='doctor-login'),

    # Kid Registration
    path('kid/register/', KidCreateView.as_view(), name='kid-register'),

    # Kid Login
    path('kid/login/', KidLoginView.as_view(), name='kid-login'),

    # Doctor's Kids List
    path('doctor/kids/', DoctorKidsListView.as_view(), name='doctor-kids'),

    # List all weeks for a specific kid
    path('kid/weeks/<int:kid_id>', KidWeekListView.as_view(), name='kid-weeks'),

    # Media Upload and Save
    path('media/upload/', MediaUploadView.as_view(), name='media-upload'),
    path('media/save/', MediaSaveView.as_view(), name='media-save'),

    # Voice Upload and Save
    path('voice/upload/', KidVoiceRecordingUploadView.as_view(), name='voice-upload'),
    path('voice/save/', KidVoiceRecordingSaveView.as_view(), name='voice-save'),

    # Doctor Feedback
    path('voice/feedback/<int:voice_id>', DoctorFeedbackCreateView.as_view(), name='doctor-feedback'),

    # Kid Media View
    path('kid/media/', KidMediaListView.as_view(), name='kid-media-list'),

    # Doctor Voices List View
    path('doctor/voice-records/', DoctorVoiceRecordsListView.as_view(), name='doctor-voice-records'),

    # Doctors List
    path('doctors/', DoctorListView.as_view(), name='doctor-list'),

    # Kid Feedback View
    path('kid/feedback/<int:kid_id>/', KidFeedbackListView.as_view(), name='kid-feedback-list'),

]
