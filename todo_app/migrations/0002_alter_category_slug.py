# Generated by Django 5.0 on 2023-12-22 15:09

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='title', unique=True),
        ),
    ]
