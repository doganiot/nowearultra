from django.urls import path
from . import views

app_name = 'visualization'

urlpatterns = [
    path('<uuid:model_id>/', views.visualize_model, name='visualize_model'),
]


