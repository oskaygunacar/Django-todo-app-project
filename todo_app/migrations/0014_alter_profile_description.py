# Generated by Django 5.0 on 2023-12-29 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0013_alter_todo_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
