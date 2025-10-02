from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import Model3D, Project
import os


def model_list(request):
    """Model listesi"""
    models = Model3D.objects.all()
    return render(request, 'models/model_list.html', {'models': models})


def model_upload(request):
    """Model yükleme"""
    if request.method == 'POST':
        # Dosya yükleme işlemi
        uploaded_file = request.FILES.get('file')
        name = request.POST.get('name', uploaded_file.name if uploaded_file else 'Yeni Model')
        
        if uploaded_file:
            # Dosya formatı kontrolü
            file_ext = os.path.splitext(uploaded_file.name)[1].lower()
            if file_ext not in ['.stl', '.ply']:
                messages.error(request, 'Sadece .stl ve .ply dosyaları desteklenmektedir.')
                return redirect('models:model_upload')
            
            # Model oluştur
            model = Model3D(
                name=name,
                original_file=uploaded_file
            )
            model.save()
            
            messages.success(request, f'Model başarıyla yüklendi: {model.name}')
            return redirect('models:model_detail', model_id=model.id)
        else:
            messages.error(request, 'Lütfen bir dosya seçin.')
    
    return render(request, 'models/model_upload.html')


def model_detail(request, model_id):
    """Model detayı"""
    model = get_object_or_404(Model3D, id=model_id)
    return render(request, 'models/model_detail.html', {'model': model})


def model_delete(request, model_id):
    """Model silme"""
    model = get_object_or_404(Model3D, id=model_id)
    
    if request.method == 'POST':
        model_name = model.name
        model.delete()
        messages.success(request, f'Model silindi: {model_name}')
        return redirect('models:model_list')
    
    return render(request, 'models/model_confirm_delete.html', {'model': model})
