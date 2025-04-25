from django.shortcuts import render, get_object_or_404
from .models import Activity

def index(request):
    upcoming_activity_list = Activity.objects.order_by('-start')[:5]
    context = { "upcoming_activity_list": upcoming_activity_list }
    return render(request, 'activities/index.html', context)

def detail(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    return render(request, 'activities/detail.html', { 'activity': activity })
