from django.contrib import admin

# Register your models here.
from talks.models import Participant, Session

admin.site.register(Participant)
admin.site.register(Session)
