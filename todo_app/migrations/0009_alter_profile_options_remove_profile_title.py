# Generated by Django 5.0 on 2023-12-25 18:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0008_alter_profile_is_active_alter_profile_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={},
        ),
        migrations.RemoveField(
            model_name='profile',
            name='title',
        ),
    ]
