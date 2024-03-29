from django.contrib import admin
from todo_app.models import Todo, Category, Images, Profile
# from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

class TodoAdmin(admin.ModelAdmin):
    list_display = ["id", 'user', "category", "title", "slug", "content", "is_active",]
    list_display_links = ["id", 'user', "category", "title", "slug", "content", "is_active",]
    # summernote_fields = ("content",)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "is_active", "user"]
    list_display_links = ["title", "slug", "is_active", "user"]

admin.site.register(Todo,TodoAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Images)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'slug', 'avatar']

# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = [
#         'username',
#         'account_create_time'
#     ]