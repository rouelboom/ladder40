from django.contrib import admin

from event.models import User, Event, TelegramUserToPasswordRelation


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'total_games', 'win_rate')


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'event_date')


class TelegramUserToPasswordRelationAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'site_access', 'last_update')


admin.site.register(User, UserAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(TelegramUserToPasswordRelation, TelegramUserToPasswordRelationAdmin)

