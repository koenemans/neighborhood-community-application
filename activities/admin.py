from django.contrib import admin

from .models import Activity

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'start', 'end')
    list_filter = ('start', 'end')
    search_fields = ('title', 'content', 'location')
    fieldsets = [
        (None, {'fields': ['title', 'content', 'committee']}),
        ('Practical Information', { 'fields': ['location', 'start', 'end'] }),
        ('Metadata', { 'fields': ['created_at', 'slug'] })
    ]
    prepopulated_fields = {'slug': ('title',)}
    

admin.site.register(Activity, ActivityAdmin)