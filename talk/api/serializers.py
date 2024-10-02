from rest_framework import serializers
from .models import Doctor, Kid, Week, Media, KidVoiceRecording, Feedback


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['job_id', 'phone', 'email', 'dob', 'full_name']


class KidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kid
        fields = ['k_id', 'name', 'dob', 'phone', 'age', 'doctor']


class WeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = Week
        fields = ['kid', 'week_number']


class MediaUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['file']


class MediaSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['week', 'url']


class KidVoiceRecordingUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = KidVoiceRecording
        fields = ['file']


class KidVoiceRecordingSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = KidVoiceRecording
        fields = ['week', 'url']


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['voice_recording', 'stars', 'note']
