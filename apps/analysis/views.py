from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from apps.models.models import Model3D, ModelAnalysis
from .services.feature_detector import FeatureDetector
import time


def analyze_model(request, model_id):
    """Model analizi başlat"""
    model = get_object_or_404(Model3D, id=model_id)
    
    try:
        # Mevcut analizi kontrol et
        if hasattr(model, 'analysis'):
            messages.info(request, 'Model zaten analiz edilmiş. Sonuçları görüntülüyorsunuz.')
            return redirect('analysis:analysis_results', model_id=model.id)
        
        # Analiz başlat
        start_time = time.time()
        detector = FeatureDetector(model.original_file.path)
        analysis_data = detector.analyze()
        
        # Analiz kaydı oluştur
        analysis = ModelAnalysis.objects.create(
            model=model,
            vertices_count=analysis_data['vertices_count'],
            faces_count=analysis_data['faces_count'],
            is_watertight=analysis_data['is_watertight'],
            volume=analysis_data.get('volume'),
            surface_area=analysis_data.get('surface_area'),
            bounding_box_min=analysis_data['bounding_box']['min'],
            bounding_box_max=analysis_data['bounding_box']['max'],
            top_points=analysis_data['top_points'],
            bottom_points=analysis_data['bottom_points'],
            sharp_points=analysis_data['sharp_points'],
            widest_area=analysis_data['widest_area'],
            narrowest_area=analysis_data['narrowest_area'],
            topology_status=analysis_data['topology_status']
        )
        
        execution_time = time.time() - start_time
        messages.success(request, f'Model başarıyla analiz edildi ({execution_time:.2f} saniye)')
        return redirect('analysis:analysis_results', model_id=model.id)
        
    except Exception as e:
        messages.error(request, f'Analiz sırasında hata oluştu: {str(e)}')
        return redirect('models:model_detail', model_id=model.id)


def analysis_results(request, model_id):
    """Analiz sonuçlarını göster"""
    model = get_object_or_404(Model3D, id=model_id)
    
    if not hasattr(model, 'analysis'):
        messages.warning(request, 'Model henüz analiz edilmemiş.')
        return redirect('analysis:analyze_model', model_id=model.id)
    
    analysis = model.analysis
    return render(request, 'analysis/analysis_results.html', {
        'model': model,
        'analysis': analysis
    })
