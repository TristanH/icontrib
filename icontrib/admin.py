from django.contrib import admin
from icontrib.models import Campaign, Contribution, UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)

admin.site.register(Campaign)
admin.site.register(Contribution)
admin.site.register(UserProfile, UserProfileAdmin)
