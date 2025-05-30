# Generated by Django 5.2 on 2025-04-28 15:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('committees', '0003_committee_slug'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='committee',
            name='contact_person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='committees', to=settings.AUTH_USER_MODEL),
        ),
    ]
