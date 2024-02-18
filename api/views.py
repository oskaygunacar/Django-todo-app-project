from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, DestroyAPIView

# rest methods
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound

from django.shortcuts import get_object_or_404


# serializer
from api.serializers import TodoSerializer, CategorySerializer

#permissions & authentication
from rest_framework import permissions
from rest_framework import authentication

#models
from todo_app.models import Todo, Category


# VIEWS

### Todos
class TodoListCreateView(ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

class TodoDetailView(RetrieveAPIView):
    serializer_class = TodoSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = Todo.objects.filter(id=self.kwargs.get('id'), user=self.request.user).first()
        if obj is not None:
            return obj
        else:
            raise NotFound({'info':'Todo not found!'})
        
class TodoDestroyView(DestroyAPIView):
    serializer_class = TodoSerializer
    lookup_field = 'id'
    queryset = Todo.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        id = self.kwargs.get('id')
        item_to_delete = Todo.objects.filter(pk=id, user=request.user).first()
        if item_to_delete:
            item_to_delete.delete()
            return Response({'Info':'Item Succesfully Deleted', 'status':'200'}, status=status.HTTP_200_OK)
        return Response({'Info':'Item not found', 'status':'404'}, status=status.HTTP_404_NOT_FOUND)
        

        

        

### Category
class CategoryListCreateView(ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Category.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

