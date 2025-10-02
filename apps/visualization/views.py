from django.shortcuts import render, get_object_or_404
from apps.models.models import Model3D


def visualize_model(request, model_id):
    """3D model görselleştirme"""
    model = get_object_or_404(Model3D, id=model_id)
    
    return render(request, 'visualization/viewer.html', {
        'model': model
    })
