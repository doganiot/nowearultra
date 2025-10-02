from django.urls import path
from . import views

app_name = 'analysis'

urlpatterns = [
    path('<uuid:model_id>/', views.analyze_model, name='analyze_model'),
    path('<uuid:model_id>/results/', views.analysis_results, name='analysis_results'),
]


