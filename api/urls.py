from django.urls import path
from api import views

app_name = 'api'

urlpatterns = [
    path('todo/', views.TodoListCreateView.as_view(), name='todo_list_create_api_view'),
    path('todo/<int:id>/', views.TodoDetailView.as_view(), name='todo_detail_view'),
    path('todo/<int:id>/delete/', views.TodoDestroyView.as_view(), name='todo_destroy_view'),
    path('category-list-create/', views.CategoryListCreateView.as_view(), name='category_list_create_api_view')
]