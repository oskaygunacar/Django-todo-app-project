from rest_framework.generics import ListCreateAPIView

# serializer
from api.serializers import TodoSerializer

#permissions
from rest_framework import permissions

#models
from todo_app.models import Todo


class ListCreateView(ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user, is_active=True)
    