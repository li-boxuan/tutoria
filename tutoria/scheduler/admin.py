from django.contrib import admin
from scheduler.models import (Session, BookingRecord)

admin.site.register(Session)
admin.site.register(BookingRecord)
