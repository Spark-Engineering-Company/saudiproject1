from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Doctor)
admin.site.register(Kid)
admin.site.register(Week)
admin.site.register(Media)
admin.site.register(KidVoiceRecording)
admin.site.register(Feedback)

