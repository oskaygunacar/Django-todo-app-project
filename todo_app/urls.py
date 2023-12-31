from django.urls import path, include
from todo_app import views

app_name = "todo_app"

urlpatterns = [
    path("tag/<slug:tag_slug>/", views.tag_detail, name="tag_detail"),
    path('category/edit/<slug:category_slug>/', views.edit_category_view, name="category_edit"),
    path('category/delete/<slug:category_slug>/', views.delete_category_view, name="delete_category"),
    path("category/<slug:category_slug>/", views.category_detail_view, name="category_detail"),
    path("todo/new-todo/", views.todo_entry_view, name='todo_entry'),
    path("todo/edit/<slug:todo_slug>/", views.edit_todo_view, name="edit_todo"),
    path("todo/create-category/", views.create_category_view, name="create_category"),
    path("todo/<slug:todo_slug>/", views.todo_view, name="todo_view" ),
    path("todo/delete/<slug:todo_slug>/", views.delete_todo_view, name="delete_todo"),
    path("", views.home_view, name="home"),
    path("complete-todo/", views.complete_todo, name="complete_todo"),
    path('activate_task/', views.activate_task, name='activate_task'),

    #Profile
    path('profile/profile-update/', views.profile_edit_view, name='profile_update'),
    path('profile/delete-account/', views.delete_account_view, name="delete_account"),
    path('profile/<slug:profile_slug>/', views.profile_view, name='profile'),
]