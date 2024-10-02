from django.db import models


class Doctor(models.Model):
    job_id = models.IntegerField(unique=True)
    phone = models.IntegerField(unique=True)
    email = models.EmailField(unique=True)
    dob = models.DateField()
    full_name = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name


# Kid model (each doctor can have multiple kids)
class Kid(models.Model):
    k_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    dob = models.DateField()
    phone = models.IntegerField(unique=True)
    age = models.IntegerField()
    doctor = models.ForeignKey(Doctor, related_name="kids", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Call the original save method
        super().save(*args, **kwargs)

        # Check if weeks are already created
        if not self.weeks.exists():
            # Create 4 weeks for the kid
            for week_number in range(1, 5):
                Week.objects.create(kid=self, week_number=week_number)


# Week model to store data for each week per kid
class Week(models.Model):
    kid = models.ForeignKey(Kid, related_name="weeks", on_delete=models.CASCADE)
    week_number = models.IntegerField()

    def __str__(self):
        return f"Week {self.week_number} for {self.kid.name}"


# Media for each week: pictures and video
class Media(models.Model):
    week = models.ForeignKey(Week, related_name="media", on_delete=models.CASCADE)
    file = models.FileField(upload_to="media/")
    url = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return f"Media File for {self.week}"


# Voice recordings from the kid to the doctor
class KidVoiceRecording(models.Model):
    week = models.ForeignKey(Week, related_name="voice_recordings", on_delete=models.CASCADE)
    file = models.FileField(upload_to="voice/")
    url = models.CharField(max_length=300, blank=True, null=True)
    feedback_state = models.BooleanField(default=False)

    def __str__(self):
        return f"Voice recording for {self.week}"


# Feedback from doctor to the kid
class Feedback(models.Model):
    voice_recording = models.OneToOneField(KidVoiceRecording, related_name="feedback", on_delete=models.CASCADE)
    stars = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    note = models.TextField()

    def __str__(self):
        return f"Feedback for {self.voice_recording}'s voice"
