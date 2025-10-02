from django.urls import path
from . import views

app_name = 'processing'

urlpatterns = [
    path('<uuid:model_id>/', views.processing_dashboard, name='processing_dashboard'),
    path('<uuid:model_id>/rotate/', views.rotate_model, name='rotate_model'),
    path('<uuid:model_id>/cut/', views.cut_model, name='cut_model'),
    path('<uuid:model_id>/smooth/', views.smooth_model, name='smooth_model'),
    path('<uuid:model_id>/fill-holes/', views.fill_holes, name='fill_holes'),
    path('<uuid:model_id>/ovalize/', views.ovalize_model, name='ovalize_model'),
    path('<uuid:model_id>/drill/', views.drill_hole, name='drill_hole'),
    # API endpoints
    path('<uuid:model_id>/save-step/', views.save_processing_step, name='save_step'),
    path('<uuid:model_id>/complete/', views.complete_processing, name='complete'),
]


