from django.contrib import admin
from .models import (Sport, Match, Session, CancelledSession)

admin.site.register(Sport)
admin.site.register(Match)
admin.site.register(Session)
admin.site.register(CancelledSession)
