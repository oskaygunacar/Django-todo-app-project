from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView, ListAPIView

# rest methods
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound


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

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

class TodoDetailView(RetrieveAPIView):
    serializer_class = TodoSerializer
    lookup_field = 'id'

    def get_object(self):
        obj = Todo.objects.filter(id=self.kwargs.get('id'), user=self.request.user).first()
        if obj is not None:
            return obj
        else:
            raise NotFound({'info':'Todo not found!'})
        
class TodoDestroyView(DestroyAPIView):

    def delete(self, request, *args, **kwargs):
        id = self.kwargs.get('id')
        item_to_delete = Todo.objects.filter(pk=id, user=request.user).first()
        if item_to_delete:
            item_to_delete.delete()
            return Response({'Info':'Item Succesfully Deleted', 'status':'200'}, status=status.HTTP_200_OK)
        return Response({'Info':'Item not found', 'status':'404'}, status=status.HTTP_404_NOT_FOUND)
        

class TodoUpdateView(UpdateAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        id = kwargs.get('id')
        obj = Todo.objects.filter(pk=id, user=request.user).first()
        if not obj:
            return Response({'info':'Instance that you are trying to update not found!', 'status':'404'}, status=status.HTTP_404_NOT_FOUND)
        super().update(request, *args, **kwargs) # UpdateAPIView default update method. It calls UpdateMixin
        return Response({'info':'Instance Succesfully Updated', 'status':'200'}, status=status.HTTP_200_OK)
        

### Category
class CategoryListCreateView(ListCreateAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        user = self.request.user
        return Category.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryDetailView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_object(self):
        id = self.kwargs.get('id')
        user = self.request.user
        try:
            obj = Category.objects.get(pk=id, user=user)
        except:
            raise NotFound({'info':'Category Instance Not Found!'})
        else:
            return obj
        
class CategoryDeleteView(DestroyAPIView):

    def delete(self, request, *args, **kwargs):
        id = kwargs.get('id')
        user = request.user
        try:
            obj = Category.objects.get(pk=id, user=user)
        except:
            return Response({'info':'Category Instance Not Found!'}, status=status.HTTP_404_NOT_FOUND)
        else:
            obj.delete()
            return Response({'info':'Category Instance Succesfully Deleted'}, status=status.HTTP_200_OK)


class CategoryUpdateView(UpdateAPIView):
    queryset = Category.objects.all()
    lookup_field = 'id'
    serializer_class = CategorySerializer

    def update(self, request, *args, **kwargs):
        try:
            obj = Category.objects.get(pk=kwargs.get('id'), user=request.user) # if there is an instance
        except:
            return Response({'info':'Category Instance Not Found!'}, status=status.HTTP_404_NOT_FOUND)
        else:
            super().update(request, *args, **kwargs)
            return Response({'info':'Category Instance Succesfully Updated'}, status=status.HTTP_200_OK)



# Category Based Todo Filtering
        
class TodoCategoryListView(ListAPIView):
    serializer_class = TodoSerializer
    lookup_field = 'slug'
    queryset = Todo.objects.all()

    def get_queryset(self):
        slug = self.kwargs.get('category_slug')
        try:
            category = Category.objects.get(slug=slug)
        except:
            # return Response({'info':'Category Instance Not Found'}) -> get query set metodunda bu şekilde Response Dönemiyoruz.
            raise NotFound({'info':'Category Instance Not Found'}, code=status.HTTP_404_NOT_FOUND)
        else:
            return category.todo_set.all()
