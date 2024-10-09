from rest_framework import serializers
from .models import Doctor, Kid, Week, Media, KidVoiceRecording, Feedback


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'


class KidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kid
        fields = ['k_id', 'name', 'dob', 'phone', 'age', 'doctor']


class WeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = Week
        fields = '__all__'


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


class KidVoiceRecordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = KidVoiceRecording
        fields = ['week', 'file', 'url', 'feedback_state', 'media_type']  # Added media_type here


class KidVoiceRecordingSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = KidVoiceRecording
        fields = ['week', 'file', 'url', 'media_type', 'feedback_state']
        read_only_fields = ['feedback_state']  # feedback_state should be read-only and default to False


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['voice_recording', 'stars', 'note']
