# Generated by Django 5.0 on 2023-12-25 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0005_alter_category_options_alter_tag_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='todo',
            options={'ordering': ('created_at',)},
        ),
    ]
