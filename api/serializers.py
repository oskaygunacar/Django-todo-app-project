from rest_framework import serializers
from todo_app.models import Category, Todo

class TodoSerializer(serializers.Serializer):
    class Meta:
        model = Todo
        fields = '__all__'
        exclude = ('tag',)