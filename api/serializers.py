from rest_framework import serializers
from todo_app.models import Category, Todo
from rest_framework.reverse import reverse

class TodoSerializer(serializers.ModelSerializer):
    created_time = serializers.SerializerMethodField()
    updated_time = serializers.SerializerMethodField()
    # category = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    api_detail_url = serializers.HyperlinkedIdentityField(view_name='api:todo_detail_view', lookup_field='id')
    api_delete_url = serializers.HyperlinkedIdentityField(view_name='api:todo_destroy_view', lookup_field='id')
    api_update_url = serializers.HyperlinkedIdentityField(view_name='api:todo_update_view', lookup_field='id')

    class Meta:
        model = Todo
        exclude = ['created_at', 'updated_at']

        """
        Method belows updating the customized SerializerMethodFields above. def get_<field_name>() structure.
        """

    def get_created_time(self, obj):
        if obj.formatted_created_at():
            return obj.formatted_created_at() if obj.formatted_created_at() else None # model own method
        else:
            return None
    
    def get_updated_time(self, obj):
        if obj.formatted_updated_at():    
            return obj.formatted_updated_at() if obj.formatted_created_at() else None # model own method
        else:
            None
    
    # def get_category(self,obj):
    #     return obj.category.title
    
    def get_user(self, obj):
        return obj.user.username # model own field

    
class CategorySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    api_category_detail = serializers.HyperlinkedIdentityField(view_name='api:category_detail_view', lookup_field='id')
    category_detail_url = serializers.SerializerMethodField()

    class Meta:
        model = Category
        exclude = ('created_time',)

    def get_user(self,obj):
        return obj.user.username
    
    def get_category_detail_url(self,obj):
        return reverse('todo_app:category_detail', kwargs={'category_slug':obj.slug})