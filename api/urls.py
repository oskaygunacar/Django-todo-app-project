from django.urls import path
from api import views

app_name = 'api'

urlpatterns = [
    path('list-create/', views.ListCreateView.as_view(), name='list_create_api_view'),
]