# Generated by Django 5.0 on 2024-02-14 22:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0015_alter_category_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todo',
            name='tag',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]