from django.urls import path
from .views import *

urlpatterns = [
    path('doctor/register/', DoctorCreateView.as_view(), name='doctor-register'),
    path('doctor/login/', DoctorLoginView.as_view(), name='doctor-login'),
    path('kid/register/', KidCreateView.as_view(), name='kid-register'),
    path('kid/login/', KidLoginView.as_view(), name='kid-login'),
    path('doctor/kids/', DoctorKidsListView.as_view(), name='doctor-kids-list'),
    path('kid/<int:kid_id>/weeks/', KidWeekListView.as_view(), name='kid-week-list'),

    # New endpoints for pictures and video uploads and saves
    path('media/pictures/upload/<int:week_id>/', PicturesUploadView.as_view(), name='pictures-upload'),
    path('media/video/upload/<int:week_id>/', VideoUploadView.as_view(), name='video-upload'),
    path('media/pictures/save/', PicturesSaveView.as_view(), name='pictures-save'),
    path('media/video/save/', VideoSaveView.as_view(), name='video-save'),

    path('voice/upload/', KidVoiceRecordingUploadView.as_view(), name='voice-upload'),
    path('voice/save/', KidVoiceRecordingSaveView.as_view(), name='voice-save'),

    path('feedback/create/<int:voice_id>/', DoctorFeedbackCreateView.as_view(), name='doctor-feedback-create'),

    # Updated endpoint for doctor to view voice recordings by week_id in URL
    path('doctor/voice-records/<int:week_id>/', DoctorVoiceRecordsListView.as_view(), name='doctor-voice-records'),

    path('media/list/<int:week_id>/', KidMediaListView.as_view(), name='kid-media-list'),
    path('doctors/', DoctorListView.as_view(), name='doctor-list'),
    path('feedback/kid/<int:kid_id>/', KidFeedbackListView.as_view(), name='kid-feedback-list'),

    path('doctor/profile/<int:job_id>/edit/', DoctorProfileEditView.as_view(), name='doctor-profile-edit'),
    path('kid/profile/<int:k_id>/edit/', KidProfileEditView.as_view(), name='kid-profile-edit'),
]
