import os
from django.core.files.storage import default_storage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import *
from talk import settings


# Utility function to format responses
def format_response(status_value, message, data=None):
    return {
        "status": status_value,
        "message": message,
        "data": data if data else None
    }


# Utility function to delete media files for a week
def delete_existing_media(week):
    media_files = Media.objects.filter(week=week)
    for media_file in media_files:
        if media_file.file and default_storage.exists(media_file.file.name):
            default_storage.delete(media_file.file.name)
    media_files.delete()


# 1- Doctor Registration View
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


# 2- Doctor Login View based on job_id
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


# 3- Kid Registration View
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


# 4- Kid Login View based on k_id (kid's ID)
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
# 5- List all kids assigned to the doctor based on job_id
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


# 6- List all weeks for a specific kid
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


# 7- Media Upload View
class MediaUploadView(APIView):
    @swagger_auto_schema(
        request_body=MediaUploadSerializer,
        responses={200: openapi.Response('Media uploaded successfully')}
    )
    def post(self, request):
        week_id = request.data.get('week_id')
        media_files = request.FILES.getlist('file')

        if not week_id:
            return Response(format_response(False, "week_id is required."), status=status.HTTP_400_BAD_REQUEST)

        try:
            week = Week.objects.get(id=week_id)

            # Validate the number of files: either 4 pictures or 1 video
            if len(media_files) == 4 and all([file.name.endswith(('jpg', 'jpeg', 'png')) for file in media_files]):
                media_type = 'pictures'
            elif len(media_files) == 1 and media_files[0].name.endswith(('mp4', 'avi', 'mov')):
                media_type = 'video'
            else:
                return Response(format_response(False, "You must upload either 4 pictures or 1 video."),
                                status=status.HTTP_400_BAD_REQUEST)

            # Delete existing media if any
            delete_existing_media(week)

            # Save new media files
            for media_file in media_files:
                file_path = os.path.join(settings.MEDIA_ROOT, media_file.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in media_file.chunks():
                        destination.write(chunk)

                # Generate URL for each file
                url = request.scheme + '://' + request.get_host() + settings.MEDIA_URL + media_file.name

                # Save each media file in the database
                Media.objects.create(week=week, file=media_file, url=url)

            return Response(format_response(True, f"{media_type.capitalize()} uploaded successfully."),
                            status=status.HTTP_200_OK)

        except Week.DoesNotExist:
            return Response(format_response(False, "Week with id not found."), status=status.HTTP_404_NOT_FOUND)


# 8- Save Media URL to Database
class MediaSaveView(APIView):
    @swagger_auto_schema(
        request_body=MediaSaveSerializer,
        responses={200: openapi.Response('Media saved successfully')}
    )
    def post(self, request):
        week_id = request.data.get('week')
        urls = request.data.getlist('url')

        if not week_id:
            return Response(format_response(False, "week_id is required."), status=status.HTTP_400_BAD_REQUEST)

        try:
            week = Week.objects.get(id=week_id)

            # Validate the number of URLs: either 4 picture URLs or 1 video URL
            if len(urls) == 4 and all([url.endswith(('jpg', 'jpeg', 'png')) for url in urls]):
                media_type = 'pictures'
            elif len(urls) == 1 and urls[0].endswith(('mp4', 'avi', 'mov')):
                media_type = 'video'
            else:
                return Response(format_response(False, "You must provide either 4 picture URLs or 1 video URL."),
                                status=status.HTTP_400_BAD_REQUEST)

            # Delete existing media if any
            delete_existing_media(week)

            # Save new media URLs
            for url in urls:
                Media.objects.create(week=week, url=url)

            return Response(format_response(True, f"{media_type.capitalize()} saved successfully."),
                            status=status.HTTP_201_CREATED)

        except Week.DoesNotExist:
            return Response(format_response(False, "Week with id not found."), status=status.HTTP_404_NOT_FOUND)


# 9- Kid uploads voice recordings for pictures and video
class KidVoiceRecordingUploadView(APIView):
    @swagger_auto_schema(
        request_body=KidVoiceRecordingUploadSerializer,
        responses={200: openapi.Response('Voice recording uploaded successfully')}
    )
    def post(self, request):
        serializer = KidVoiceRecordingUploadSerializer(data=request.data)
        if serializer.is_valid():
            voice_file = serializer.validated_data['file']
            week_id = request.data.get('week_id')
            media_type = request.data.get('media_type')  # Should be either 'pictures' or 'video'

            # Check if media_type is valid
            if media_type not in ['pictures', 'video']:
                return Response(format_response(False, "Invalid media_type. Must be 'pictures' or 'video'."),
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                week = Week.objects.get(id=week_id)
            except Week.DoesNotExist:
                return Response(format_response(False, "Week with id not found."), status=status.HTTP_404_NOT_FOUND)

            # Save the voice file in the MEDIA_ROOT
            file_path = os.path.join(settings.MEDIA_ROOT, voice_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in voice_file.chunks():
                    destination.write(chunk)

            # Generate the URL for the file
            url = request.scheme + '://' + request.get_host() + settings.MEDIA_URL + voice_file.name

            # Save the voice recording
            KidVoiceRecording.objects.create(week=week, file=voice_file, url=url, feedback_state=False, media_type=media_type)

            return Response(format_response(True, "Voice recording uploaded successfully.", {'url': url}),
                            status=status.HTTP_200_OK)
        return Response(format_response(False, "Invalid data.", serializer.errors),
                        status=status.HTTP_400_BAD_REQUEST)


# 10- Save Voice Recording URL to Database
class KidVoiceRecordingSaveView(APIView):
    @swagger_auto_schema(
        request_body=KidVoiceRecordingSaveSerializer,
        responses={200: openapi.Response('Voice recording saved successfully')}
    )
    def post(self, request):
        serializer = KidVoiceRecordingSaveSerializer(data=request.data)
        if serializer.is_valid():
            week_id = request.data.get('week')
            media_type = request.data.get('media_type')  # should be either 'pictures' or 'video'

            # Ensure media_type is valid
            if media_type not in ['pictures', 'video']:
                return Response(format_response(False, "Invalid media_type. Must be 'pictures' or 'video'."),
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                week = Week.objects.get(id=week_id)
            except Week.DoesNotExist:
                return Response(format_response(False, "Week with id not found."), status=status.HTTP_404_NOT_FOUND)

            # Save the voice recording
            KidVoiceRecording.objects.create(
                week=week,
                file=serializer.validated_data['file'],
                url=serializer.validated_data['url'],
                feedback_state=False,  # Default to no feedback yet
                media_type=media_type
            )

            return Response(format_response(True, "Voice recording saved successfully."),
                            status=status.HTTP_201_CREATED)
        return Response(format_response(False, "Invalid data.", serializer.errors),
                        status=status.HTTP_400_BAD_REQUEST)


# 11- Doctor gives feedback on kid's voice recordings (pictures and video separately)
class DoctorFeedbackCreateView(APIView):
    @swagger_auto_schema(request_body=FeedbackSerializer)
    def post(self, request, voice_id):
        try:
            # Fetch the voice recording
            voice_recording = KidVoiceRecording.objects.get(id=voice_id)

            # Check if feedback has already been provided
            if voice_recording.feedback_state:
                return Response(format_response(False, "Feedback has already been provided for this voice recording."),
                                status=status.HTTP_400_BAD_REQUEST)

            # Proceed with feedback creation if no feedback has been provided
            data = request.data.copy()
            data['voice_recording'] = voice_recording.id

            # Validate the serializer
            serializer = FeedbackSerializer(data=data)
            if serializer.is_valid():
                feedback = serializer.save()

                # Update the feedback_state to prevent multiple feedback
                voice_recording.feedback_state = True
                voice_recording.save()

                return Response(
                    format_response(True, "Feedback added successfully.", FeedbackSerializer(feedback).data),
                    status=status.HTTP_201_CREATED)

            return Response(format_response(False, "Error adding feedback.", serializer.errors),
                            status=status.HTTP_400_BAD_REQUEST)

        except KidVoiceRecording.DoesNotExist:
            return Response(format_response(False, "Voice recording not found."), status=status.HTTP_404_NOT_FOUND)


# 12- Doctor gets voice records uploaded by the kid using week_id
class DoctorVoiceRecordsListView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('week_id', openapi.IN_QUERY, description="Week ID", type=openapi.TYPE_INTEGER)]
    )
    def get(self, request):
        week_id = request.GET.get('week_id')

        if not week_id:
            return Response(format_response(False, "week_id is required."), status=status.HTTP_400_BAD_REQUEST)

        try:
            week = Week.objects.get(id=week_id)
            voice_records = KidVoiceRecording.objects.filter(week=week)

            if not voice_records.exists():
                return Response(format_response(False, "No voice recordings found for this week."),
                                status=status.HTTP_404_NOT_FOUND)

            serializer = KidVoiceRecordingSaveSerializer(voice_records, many=True)
            return Response(format_response(True, "Voice records fetched successfully.", serializer.data),
                            status=status.HTTP_200_OK)

        except Week.DoesNotExist:
            return Response(format_response(False, "Week with id not found."), status=status.HTTP_404_NOT_FOUND)


# 13- Kid gets pictures and video for the week using week_id
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

            if not media_files.exists():
                return Response(format_response(False, "No media found for this week."), status=status.HTTP_404_NOT_FOUND)

            # Separate pictures and video
            pictures = [media.url for media in media_files if media.file.name.endswith(('jpg', 'jpeg', 'png'))]
            video = [media.url for media in media_files if media.file.name.endswith(('mp4', 'avi', 'mov'))]

            # Check if there are exactly 4 pictures and 1 video
            if len(pictures) == 4 and len(video) == 1:
                response_data = {
                    "pictures": pictures,
                    "video": video[0]
                }
                return Response(format_response(True, "Media files fetched successfully.", response_data),
                                status=status.HTTP_200_OK)
            else:
                return Response(format_response(False, "The week must contain exactly 4 pictures and 1 video."),
                                status=status.HTTP_400_BAD_REQUEST)

        except Week.DoesNotExist:
            return Response(format_response(False, "Week with id not found."), status=status.HTTP_404_NOT_FOUND)


# 14- List all doctors for kid registration
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


# 15- List of the voices feedbacks
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


# 16- Doctor Profile Edit View
class DoctorProfileEditView(APIView):
    @swagger_auto_schema(request_body=DoctorSerializer)
    def put(self, request, job_id):
        try:
            doctor = Doctor.objects.get(job_id=job_id)
        except Doctor.DoesNotExist:
            return Response(format_response(False, "Doctor not found."), status=status.HTTP_404_NOT_FOUND)

        serializer = DoctorSerializer(doctor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(format_response(True, "Doctor profile updated successfully.", serializer.data),
                            status=status.HTTP_200_OK)
        return Response(format_response(False, "Error updating profile.", serializer.errors),
                        status=status.HTTP_400_BAD_REQUEST)


# 17- Kid Profile Edit View
class KidProfileEditView(APIView):
    @swagger_auto_schema(request_body=KidSerializer)
    def put(self, request, k_id):
        try:
            kid = Kid.objects.get(k_id=k_id)
        except Kid.DoesNotExist:
            return Response(format_response(False, "Kid not found."), status=status.HTTP_404_NOT_FOUND)

        serializer = KidSerializer(kid, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(format_response(True, "Kid profile updated successfully.", serializer.data),
                            status=status.HTTP_200_OK)
        return Response(format_response(False, "Error updating profile.", serializer.errors),
                        status=status.HTTP_400_BAD_REQUEST)