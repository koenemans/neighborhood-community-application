# Generated by Django 5.2 on 2025-04-28 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('committees', '0002_alter_committee_contact_person'),
    ]

    operations = [
        migrations.AddField(
            model_name='committee',
            name='slug',
            field=models.SlugField(default='abc', max_length=200, unique=True),
            preserve_default=False,
        ),
    ]
