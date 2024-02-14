from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import User
from tinymce import models as tinymce_models
from django.urls import reverse
import random, string

from django.utils.timezone import localtime

from slugify import slugify

# Base model
class BaseModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title', unique=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        abstract=True
        ordering=('title',)


class Category(BaseModel):
    created_time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_abso_url(self):
        return reverse(
            'todo_app:category_detail',
            kwargs={
                "category_slug": self.slug
            }
        )


class Todo(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    content = tinymce_models.HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_abso_url(self):
        return reverse(
            'todo_app:todo_view',
            kwargs={
                "todo_slug": self.slug
            }
        )
    
    class Meta:
        ordering = ('created_at',)

    def formatted_created_at(self):
        return localtime(self.created_at).strftime('%Y-%m-%d %H:%M')

    def formatted_updated_at(self):
        return localtime(self.updated_at).strftime('%Y-%m-%d %H:%M')


class Images(models.Model):
    image = models.ImageField(upload_to='todo-uploads/')



# Profile Model Section
def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=125, unique=True)
    is_active = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            if not Profile.objects.filter(slug=slugify(f"{self.user.username} {self.user.last_name}")).exists():
                self.slug = slugify(f"{self.user.username} {self.user.last_name}")
            else:
                self.slug = slugify(f"{self.user.username} {self.user.last_name} {rand_slug()}")
        super(Profile, self).save(*args, **kwargs)

    def get_abso_url(self):
        return reverse('todo_app:profile', kwargs={'profile_slug':self.slug})