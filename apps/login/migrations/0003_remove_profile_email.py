# Generated by Django 2.1.2 on 2018-10-29 08:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_profile_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
    ]