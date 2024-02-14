from rest_framework import serializers
from todo_app.models import Category, Todo

class TodoSerializer(serializers.ModelSerializer):
    created_time = serializers.SerializerMethodField()
    updated_time = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Todo
        exclude = ['content','created_at', 'updated_at']

    def get_created_time(self, obj):
        return obj.formatted_created_at() # model own method
    
    def get_updated_time(self, obj):
        return obj.formatted_updated_at() # model own method
    
    def get_category(self,obj):
        return obj.category.title # model own field
