from django.urls import path
from api import views

app_name = 'api'

urlpatterns = [
    path('todo/', views.TodoListCreateView.as_view(), name='todo_list_create_api_view'), # list create todo
    path('todo/<int:id>/', views.TodoDetailView.as_view(), name='todo_detail_view'), # todo detail
    path('todo/<int:id>/delete/', views.TodoDestroyView.as_view(), name='todo_destroy_view'), # delete todo
    path('todo/<int:id>/update/', views.TodoUpdateView.as_view(), name='todo_update_view'), # update todo
    path('todo/<slug:category_slug>/', views.TodoCategoryListView.as_view(), name='todo_category_list_view'), # category based todo filtering url
    # Categories
    path('category/', views.CategoryListCreateView.as_view(), name='category_list_create_api_view'), # list create
    path('category/<int:id>/', views.CategoryDetailView.as_view(), name='category_detail_view'), # detail
    path('category/<int:id>/delete/', views.CategoryDeleteView.as_view(), name='category_delete_view'), # delete category
    path('category/<int:id>/update/', views.CategoryUpdateView.as_view(), name='category_update_view'), # update category
]