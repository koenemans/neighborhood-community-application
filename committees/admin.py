from django.contrib import admin

from .models import Committee

class CommitteeAdmin(admin.ModelAdmin):
    list_display = ('group', 'email', 'contact_person')
    search_fields = ('group', 'email', 'contact_person')
    fieldsets = [
        (None, {'fields': ['group', 'email', 'contact_person', 'description']}),
    ]

admin.site.register(Committee, CommitteeAdmin)
