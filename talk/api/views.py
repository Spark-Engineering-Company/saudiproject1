import os

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import *
from .serializers import *
from talk import settings


# Utility function to format responses
def format_response(status_value, message, data=None):
    return {
        "status": status_value,
        "message": message,
        "data": data if data else None
    }


# Doctor Registration View
class DoctorCreateView(APIView):
    @swagger_auto_schema(request_body=DoctorSerializer)
    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            doctor = serializer.save()
            return Response(format_response(True, "Doctor created successfully.", DoctorSerializer(doctor).data),
                            status=status.HTTP_201_CREATED)
        return Response(format_response(False, "Error creating doctor.", serializer.errors),
                        status=status.HTTP_400_BAD_REQUEST)


# Doctor Login View based on job_id
class DoctorLoginView(APIView):
    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('job_id', openapi.IN_QUERY, description="Doctor's job ID", type=openapi.TYPE_STRING)]
    )
    def post(self, request):
        job_id = request.data.get('job_id')
        if not job_id:
            return Response(format_response(False, "job_id is required."), status=status.HTTP_400_BAD_REQUEST)

        try:
            doctor = Doctor.objects.get(job_id=job_id)
            serializer = DoctorSerializer(doctor)
            return Response(format_response(True, "Login successful.", serializer.data), status=status.HTTP_200_OK)
        except Doctor.DoesNotExist:
            return Response(format_response(False, "Doctor with job_id not found."), status=status.HTTP_404_NOT_FOUND)


# Kid Registration View
class KidCreateView(APIView):
    @swagger_auto_schema(request_body=KidSerializer)
    def post(self, request):
        serializer = KidSerializer(data=request.data)
        if serializer.is_valid():
            kid = serializer.save()
            return Response(format_response(True, "Kid created successfully.", KidSerializer(kid).data),
                            status=status.HTTP_201_CREATED)
        return Response(format_response(False, "Error creating kid.", serializer.errors),
                        status=status.HTTP_400_BAD_REQUEST)


# Kid Login View based on k_id (kid's ID)
class KidLoginView(APIView):
    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('k_id', openapi.IN_QUERY, description="Kid's ID", type=openapi.TYPE_STRING)]
    )
    def post(self, request):
        k_id = request.data.get('k_id')
        if not k_id:
            return Response(format_response(False, "k_id is required."), status=status.HTTP_400_BAD_REQUEST)

        try:
            kid = Kid.objects.get(k_id=k_id)
            serializer = KidSerializer(kid)
            return Response(format_response(True, "Login successful.", serializer.data), status=status.HTTP_200_OK)
        except Kid.DoesNotExist:
            return Response(format_response(False, "Kid with id not found."), status=status.HTTP_404_NOT_FOUND)


# Doctor Views:
# List all kids assigned to the doctor based on job_id
class DoctorKidsListView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'job_id': openapi.Schema(type=openapi.TYPE_STRING, description="Doctor's job ID")
            },
            required=['job_id']
        )
    )
    def post(self, request):
        job_id = request.data.get('job_id')  # Get job_id from the request body
        if not job_id:
            return Response(format_response(False, "job_id is required."), status=status.HTTP_400_BAD_REQUEST)

        try:
            doctor = Doctor.objects.get(job_id=job_id)
            kids = Kid.objects.filter(doctor=doctor)
            serializer = KidSerializer(kids, many=True)
            return Response(format_response(True, "Kids fetched successfully.", serializer.data),
                            status=status.HTTP_200_OK)
        except Doctor.DoesNotExist:
            return Response(format_response(False, "Doctor with job_id not found."), status=status.HTTP_404_NOT_FOUND)


# List all weeks for a specific kid
class KidWeekListView(APIView):
    @swagger_auto_schema(manual_parameters=[openapi.Parameter('kid_id', openapi.IN_QUERY, description="Kid's ID", type=openapi.TYPE_INTEGER)])
    def get(self, request, kid_id):
        try:
            weeks = Week.objects.filter(kid_id=kid_id)
            serializer = WeekSerializer(weeks, many=True)
            return Response(format_response(True, "Weeks fetched successfully.", serializer.data),
                            status=status.HTTP_200_OK)
        except Kid.DoesNotExist:
            return Response(format_response(False, "Kid not found."), status=status.HTTP_404_NOT_FOUND)


# Media Upload View
class MediaUploadView(APIView):
    @swagger_auto_schema(
        request_body=MediaUploadSerializer,
        responses={200: openapi.Response('Media uploaded successfully')}
    )
    def post(self, request):
        serializer = MediaUploadSerializer(data=request.data)
        if serializer.is_valid():
            media_file = serializer.validated_data['file']
            # Save the media file in the MEDIA_ROOT
            from talk import settings
            file_path = os.path.join(settings.MEDIA_ROOT, media_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in media_file.chunks():
                    destination.write(chunk)

            # Generate the URL for the file
            url = f'/{file_path}'

            return Response(format_response(True, "Media uploaded successfully.", {'url': url}),
                            status=status.HTTP_200_OK)
        return Response(format_response(False, "Invalid data.", serializer.errors),
                        status=status.HTTP_400_BAD_REQUEST)


# Save Media URL to Database
class MediaSaveView(APIView):
    @swagger_auto_schema(
        request_body=MediaSaveSerializer,
        responses={200: openapi.Response('Media saved successfully')}
    )
    def post(self, request):
        serializer = MediaSaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(format_response(True, "Media saved successfully."), status=status.HTTP_201_CREATED)
        return Response(format_response(False, "Invalid data.", serializer.errors),
                        status=status.HTTP_400_BAD_REQUEST)


# Voice Recording Upload View
class KidVoiceRecordingUploadView(APIView):
    @swagger_auto_schema(
        request_body=KidVoiceRecordingUploadSerializer,
        responses={200: openapi.Response('Voice recording uploaded successfully')}
    )
    def post(self, request):
        serializer = KidVoiceRecordingUploadSerializer(data=request.data)
        if serializer.is_valid():
            voice_file = serializer.validated_data['file']
            # Save the voice file in the MEDIA_ROOT
            file_path = os.path.join(settings.MEDIA_ROOT, voice_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in voice_file.chunks():
                    destination.write(chunk)

            # Generate the URL for the file
            url = f'/{file_path}'

            return Response(format_response(True, "Voice recording uploaded successfully.", {'url': url}),
                            status=status.HTTP_200_OK)
        return Response(format_response(False, "Invalid data.", serializer.errors),
                        status=status.HTTP_400_BAD_REQUEST)


# Save Voice Recording URL to Database
class KidVoiceRecordingSaveView(APIView):
    @swagger_auto_schema(
        request_body=KidVoiceRecordingSaveSerializer,
        responses={200: openapi.Response('Voice recording saved successfully')}
    )
    def post(self, request):
        serializer = KidVoiceRecordingSaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(format_response(True, "Voice recording saved successfully."), status=status.HTTP_201_CREATED)
        return Response(format_response(False, "Invalid data.", serializer.errors),
                        status=status.HTTP_400_BAD_REQUEST)


# Doctor gives feedback on kid's voice recordings
class DoctorFeedbackCreateView(APIView):
    @swagger_auto_schema(request_body=FeedbackSerializer)
    def post(self, request, voice_id):
        try:
            voice_recording = KidVoiceRecording.objects.get(id=voice_id)
            data = request.data.copy()
            data['voice_recording'] = voice_recording.id

            # Validate the serializer
            serializer = FeedbackSerializer(data=data)
            if serializer.is_valid():
                feedback = serializer.save()

                # Update the feedback_state for the voice recording
                voice_recording.feedback_state = True
                voice_recording.save()

                return Response(
                    format_response(True, "Feedback added successfully.", FeedbackSerializer(feedback).data),
                    status=status.HTTP_201_CREATED)

            return Response(format_response(False, "Error adding feedback.", serializer.errors),
                            status=status.HTTP_400_BAD_REQUEST)
        except KidVoiceRecording.DoesNotExist:
            return Response(format_response(False, "Voice recording not found."), status=status.HTTP_404_NOT_FOUND)


# Doctor gets voice records uploaded by the kid using week_id
class DoctorVoiceRecordsListView(APIView):
    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('week_id', openapi.IN_QUERY, description="Week ID", type=openapi.TYPE_INTEGER)]
    )
    def get(self, request):
        week_id = request.GET.get('week_id')
        if not week_id:
            return Response(format_response(False, "week_id is required."), status=status.HTTP_400_BAD_REQUEST)

        try:
            week = Week.objects.get(id=week_id)
            voice_records = KidVoiceRecording.objects.filter(week=week)
            serializer = KidVoiceRecordingSaveSerializer(voice_records, many=True)
            return Response(format_response(True, "Voice records fetched successfully.", serializer.data),
                            status=status.HTTP_200_OK)
        except Week.DoesNotExist:
            return Response(format_response(False, "Week with id not found."), status=status.HTTP_404_NOT_FOUND)


# Kid gets pictures and videos uploaded by the doctor using week_id
class KidMediaListView(APIView):
    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('week_id', openapi.IN_QUERY, description="Week ID", type=openapi.TYPE_INTEGER)]
    )
    def get(self, request):
        week_id = request.GET.get('week_id')
        if not week_id:
            return Response(format_response(False, "week_id is required."), status=status.HTTP_400_BAD_REQUEST)

        try:
            week = Week.objects.get(id=week_id)
            media_files = Media.objects.filter(week=week)
            serializer = MediaSaveSerializer(media_files, many=True)
            return Response(format_response(True, "Media files fetched successfully.", serializer.data),
                            status=status.HTTP_200_OK)
        except Week.DoesNotExist:
            return Response(format_response(False, "Week with id not found."), status=status.HTTP_404_NOT_FOUND)


# List all doctors for kid registration
class DoctorListView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve a list of doctors",
        responses={200: DoctorSerializer(many=True)}
    )
    def get(self, request):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response({
            "status": True,
            "message": "Doctors fetched successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


# List of the voices feedbacks
class KidFeedbackListView(APIView):
    @swagger_auto_schema(responses={200: FeedbackSerializer(many=True)})
    def get(self, request, kid_id):
        # Get all voice recordings for the kid
        voice_recordings = KidVoiceRecording.objects.filter(week__kid__k_id=kid_id)

        feedback_list = []
        for voice_recording in voice_recordings:
            try:
                # Try to get the associated feedback
                feedback = voice_recording.feedback
                feedback_data = FeedbackSerializer(feedback).data
                feedback_list.append(feedback_data)
            except Feedback.DoesNotExist:
                continue  # Skip if no feedback exists for this voice recording

        if feedback_list:
            return Response(format_response(True, "Feedback fetched successfully.", feedback_list),
                            status=status.HTTP_200_OK)
        else:
            return Response(format_response(False, "No feedback found for this kid."),
                            status=status.HTTP_404_NOT_FOUND)