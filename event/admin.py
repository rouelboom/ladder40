from django.contrib import admin

from event.models import User, Event


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'total_games', 'win_rate')


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'event_date')


admin.site.register(User, UserAdmin)
admin.site.register(Event, EventAdmin)
