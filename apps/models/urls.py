from django.urls import path
from . import views

app_name = 'models'

urlpatterns = [
    path('', views.model_list, name='model_list'),
    path('upload/', views.model_upload, name='model_upload'),
    path('<uuid:model_id>/', views.model_detail, name='model_detail'),
    path('<uuid:model_id>/delete/', views.model_delete, name='model_delete'),
]


