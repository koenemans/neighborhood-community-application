from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, render
from .models import SiteConfiguration
from .forms import SiteConfigurationForm


@staff_member_required
def settings_view(request):
    config = SiteConfiguration.objects.first()
    if config is None:
        config = SiteConfiguration.objects.create()

    if request.method == "POST":
        form = SiteConfigurationForm(request.POST, request.FILES, instance=config)
        if form.is_valid():
            form.save()
            return redirect("siteconfig:settings")
    else:
        form = SiteConfigurationForm(instance=config)

    return render(request, "siteconfig/settings_form.html", {"form": form})
