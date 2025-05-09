from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import Activity

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'start', 'end')
    list_filter = ('start', 'end')
    search_fields = ('title', 'content', 'location')
    fieldsets = [
        (None, {'fields': ['title', 'content', 'committee']}),
        ('Practical Information', { 'fields': ['location', 'start', 'end'] }),
        ('Image', {'fields': ['poster']}),
        ('Metadata', { 'fields': ['created_at'] })
    ]

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start')
        end = cleaned_data.get('end')
        if start and end:
            if end < start:
                raise ValidationError(
                    "End date %(end)s cannot be before the start date %(start)s",
                    code='invalid',
                    params={'end': end, 'start': start},
                )
        return cleaned_data

admin.site.register(Activity, ActivityAdmin)