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

    # Doctor Account Management
    # -------------------------
    path('doctor/register/', DoctorCreateView.as_view(), name='doctor_register'),
    # Doctor registration with job_id
    path('doctor/login/', DoctorLoginView.as_view(), name='doctor_login'),
    # Doctor login with job_id

    # Kid Account Management
    # ----------------------
    path('kid/register/', KidCreateView.as_view(), name='kid_register'),
    # Kid registration
    path('kid/login/', KidLoginView.as_view(), name='kid_login'),
    # Kid login with k_id

    # Profile Editing
    # ---------------
    path('doctor/<str:job_id>/edit/', DoctorProfileEditView.as_view(), name='doctor_profile_edit'),
    # Edit doctor profile by job_id
    path('kid/<str:k_id>/edit/', KidProfileEditView.as_view(), name='kid_profile_edit'),
    # Edit kid profile by k_id

    # Doctor-Kid Interaction
    # ----------------------
    path('doctor/kids/', DoctorKidsListView.as_view(), name='doctor_kids_list'),
    # List all kids assigned to a specific doctor
    path('kid/<int:kid_id>/weeks/', KidWeekListView.as_view(), name='kid_week_list'),
    # List all weeks for a specific kid

    # Media Upload & Management
    # -------------------------
    path('media/upload/', MediaUploadView.as_view(), name='media_upload'),
    # Media file upload
    path('media/save/', MediaSaveView.as_view(), name='media_save'),
    # Save uploaded media URL to database

    # Voice Recording Upload & Management
    # -----------------------------------
    path('voice/upload/', KidVoiceRecordingUploadView.as_view(), name='voice_recording_upload'),
    # Kid uploads voice recording
    path('voice/save/', KidVoiceRecordingSaveView.as_view(), name='voice_recording_save'),
    # Save voice recording URL to database

    # Doctor Feedback
    # ---------------
    path('voice/<int:voice_id>/feedback/', DoctorFeedbackCreateView.as_view(), name='doctor_feedback'),
    # Doctor adds feedback for kid's voice recording
    path('kid/<int:kid_id>/feedback/', KidFeedbackListView.as_view(), name='kid_feedback_list'),
    # List all feedback for a specific kid's voice recordings

    # Doctor View Kid's Voice Records and Media
    # -----------------------------------------
    path('doctor/voice-records/', DoctorVoiceRecordsListView.as_view(), name='doctor_voice_records_list'),
    # List voice recordings submitted by kid for a specific week
    path('kid/media/', KidMediaListView.as_view(), name='kid_media_list'),
    # Kid views media files uploaded by doctor for a specific week

    # General List Views
    # ------------------
    path('doctors/', DoctorListView.as_view(), name='doctor_list'),
    # List all doctors for kid registration
]
