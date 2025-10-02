from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from apps.models.models import Model3D, ProcessingStep


def processing_dashboard(request, model_id):
    """İşleme kontrol paneli"""
    model = get_object_or_404(Model3D, id=model_id)
    steps = model.processing_steps.all()
    
    # İşlem istatistikleri
    stats = {
        'total_steps': steps.count(),
        'rotation_count': steps.filter(step_type='rotation').count(),
        'cutting_count': steps.filter(step_type='cutting').count(),
        'fill_holes_count': steps.filter(step_type='fill_holes').count(),
        'smoothing_count': steps.filter(step_type='smoothing').count(),
        'ovalization_count': steps.filter(step_type='ovalization').count(),
        'drilling_count': steps.filter(step_type='drilling').count(),
    }
    
    return render(request, 'processing/dashboard.html', {
        'model': model,
        'steps': steps,
        'stats': stats
    })


def rotate_model(request, model_id):
    """Model döndürme"""
    model = get_object_or_404(Model3D, id=model_id)
    
    if request.method == 'POST':
        try:
            from .services import ModelProcessor
            import time
            import os
            from django.core.files import File
            
            # Parametreleri al
            data = json.loads(request.body)
            x_angle = float(data.get('x_angle', 0))
            y_angle = float(data.get('y_angle', 0))
            z_angle = float(data.get('z_angle', 0))
            
            # İşleme başlama zamanı
            start_time = time.time()
            
            # Model işlemcisini başlat
            processor = ModelProcessor(model.original_file.path)
            
            # Döndürme işlemini uygula
            success = processor.rotate_model(
                x_angle=x_angle,
                y_angle=y_angle,
                z_angle=z_angle
            )
            
            if not success:
                return JsonResponse({
                    'success': False,
                    'error': 'Döndürme işlemi başarısız oldu'
                }, status=400)
            
            # Döndürülmüş modeli kaydet
            temp_path = processor.save_stl()
            
            # ProcessingStep oluştur
            step = ProcessingStep.objects.create(
                model=model,
                step_type='rotation',
                parameters={
                    'x_angle': x_angle,
                    'y_angle': y_angle,
                    'z_angle': z_angle
                },
                execution_time=time.time() - start_time,
                success=True
            )
            
            # Dosyayı ProcessingStep'e kaydet
            with open(temp_path, 'rb') as f:
                step.result_file.save(
                    f'rotate_{model.id}_{step.id}.stl',
                    File(f),
                    save=True
                )
            
            # Temp dosyayı sil
            os.unlink(temp_path)
            
            # Orijinal model dosyasını güncelle
            with open(step.result_file.path, 'rb') as f:
                model.original_file.save(
                    model.original_file.name,
                    File(f),
                    save=True
                )
            
            messages.success(request, f'Döndürme işlemi başarıyla tamamlandı! ({step.execution_time:.2f} saniye)')
            
            return JsonResponse({
                'success': True,
                'step_id': str(step.id),
                'message': 'Model başarıyla döndürüldü ve kaydedildi',
                'redirect_url': f'/processing/{model.id}/'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return render(request, 'processing/rotate.html', {'model': model})


def cut_model(request, model_id):
    """Model kesme"""
    model = get_object_or_404(Model3D, id=model_id)
    
    if request.method == 'POST':
        try:
            from .services import ModelProcessor
            import time
            import os
            from django.core.files import File
            
            # Parametreleri al
            data = json.loads(request.body)
            plane = data.get('cut_plane', 'xy')
            position = float(data.get('position', 50))
            direction = data.get('direction', 'above')
            tilt_x = float(data.get('tilt_x', 0))
            tilt_y = float(data.get('tilt_y', 0))
            
            # İşleme başlama zamanı
            start_time = time.time()
            
            # Model işlemcisini başlat
            processor = ModelProcessor(model.original_file.path)
            
            # Kesme işlemini uygula
            success = processor.cut_model(
                plane=plane,
                position=position,
                direction=direction,
                tilt_x=tilt_x,
                tilt_y=tilt_y
            )
            
            if not success:
                return JsonResponse({
                    'success': False,
                    'error': 'Kesme işlemi başarısız oldu'
                }, status=400)
            
            # Kesilmiş modeli kaydet
            temp_path = processor.save_stl()
            
            # ProcessingStep oluştur
            step = ProcessingStep.objects.create(
                model=model,
                step_type='cutting',
                parameters={
                    'cut_plane': plane,
                    'position': position,
                    'direction': direction,
                    'tilt_x': tilt_x,
                    'tilt_y': tilt_y
                },
                execution_time=time.time() - start_time,
                success=True
            )
            
            # Dosyayı ProcessingStep'e kaydet
            with open(temp_path, 'rb') as f:
                step.result_file.save(
                    f'cut_{model.id}_{step.id}.stl',
                    File(f),
                    save=True
                )
            
            # Temp dosyayı sil
            os.unlink(temp_path)
            
            # Orijinal model dosyasını güncelle (kesilmiş versiyonla değiştir)
            with open(step.result_file.path, 'rb') as f:
                model.original_file.save(
                    model.original_file.name,
                    File(f),
                    save=True
                )
            
            messages.success(request, f'Kesme işlemi başarıyla tamamlandı! ({step.execution_time:.2f} saniye)')
            
            return JsonResponse({
                'success': True,
                'step_id': str(step.id),
                'message': 'Model başarıyla kesildi ve kaydedildi',
                'redirect_url': f'/processing/{model.id}/'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return render(request, 'processing/cut.html', {'model': model})


def smooth_model(request, model_id):
    """Model yumuşatma"""
    model = get_object_or_404(Model3D, id=model_id)
    
    if request.method == 'POST':
        try:
            from .services import ModelProcessor
            import time
            import os
            from django.core.files import File
            
            # Parametreleri al
            data = json.loads(request.body)
            algorithm = data.get('algorithm', 'laplacian')
            intensity = int(data.get('intensity', 5))
            iterations = int(data.get('iterations', 10))
            preserve_edges = data.get('preserve_edges', True)
            
            # İşleme başlama zamanı
            start_time = time.time()
            
            # Model işlemcisini başlat
            processor = ModelProcessor(model.original_file.path)
            
            # Yumuşatma işlemini uygula
            success = processor.smooth_model(iterations=iterations)
            
            if not success:
                return JsonResponse({
                    'success': False,
                    'error': 'Yumuşatma işlemi başarısız oldu'
                }, status=400)
            
            # Yumuşatılmış modeli kaydet
            temp_path = processor.save_stl()
            
            # ProcessingStep oluştur
            step = ProcessingStep.objects.create(
                model=model,
                step_type='smoothing',
                parameters={
                    'algorithm': algorithm,
                    'intensity': intensity,
                    'iterations': iterations,
                    'preserve_edges': preserve_edges
                },
                execution_time=time.time() - start_time,
                success=True
            )
            
            # Dosyayı ProcessingStep'e kaydet
            with open(temp_path, 'rb') as f:
                step.result_file.save(
                    f'smooth_{model.id}_{step.id}.stl',
                    File(f),
                    save=True
                )
            
            # Temp dosyayı sil
            os.unlink(temp_path)
            
            # Orijinal model dosyasını güncelle
            with open(step.result_file.path, 'rb') as f:
                model.original_file.save(
                    model.original_file.name,
                    File(f),
                    save=True
                )
            
            messages.success(request, f'Yumuşatma işlemi başarıyla tamamlandı! ({step.execution_time:.2f} saniye)')
            
            return JsonResponse({
                'success': True,
                'step_id': str(step.id),
                'message': 'Model başarıyla yumuşatıldı ve kaydedildi',
                'redirect_url': f'/processing/{model.id}/'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return render(request, 'processing/smooth.html', {'model': model})


def fill_holes(request, model_id):
    """Delik doldurma"""
    model = get_object_or_404(Model3D, id=model_id)
    return render(request, 'processing/fill_holes.html', {'model': model})


def ovalize_model(request, model_id):
    """Ovalleştirme"""
    model = get_object_or_404(Model3D, id=model_id)
    
    if request.method == 'POST':
        try:
            from .services import ModelProcessor
            import time
            import os
            from django.core.files import File
            
            # Parametreleri al
            data = json.loads(request.body)
            intensity = int(data.get('intensity', 5))
            region = data.get('region', 'all')
            preserve_edges = data.get('preserve_edges', True)
            
            # İşleme başlama zamanı
            start_time = time.time()
            
            # Model işlemcisini başlat
            processor = ModelProcessor(model.original_file.path)
            
            # Ovalleştirme işlemini uygula
            success = processor.ovalize_model(
                intensity=intensity,
                preserve_edges=preserve_edges
            )
            
            if not success:
                return JsonResponse({
                    'success': False,
                    'error': 'Ovalleştirme işlemi başarısız oldu'
                }, status=400)
            
            # Ovalleştirilmiş modeli kaydet
            temp_path = processor.save_stl()
            
            # ProcessingStep oluştur
            step = ProcessingStep.objects.create(
                model=model,
                step_type='ovalization',
                parameters={
                    'intensity': intensity,
                    'region': region,
                    'preserve_edges': preserve_edges
                },
                execution_time=time.time() - start_time,
                success=True
            )
            
            # Dosyayı ProcessingStep'e kaydet
            with open(temp_path, 'rb') as f:
                step.result_file.save(
                    f'ovalize_{model.id}_{step.id}.stl',
                    File(f),
                    save=True
                )
            
            # Temp dosyayı sil
            os.unlink(temp_path)
            
            # Orijinal model dosyasını güncelle
            with open(step.result_file.path, 'rb') as f:
                model.original_file.save(
                    model.original_file.name,
                    File(f),
                    save=True
                )
            
            messages.success(request, f'Ovalleştirme işlemi başarıyla tamamlandı! ({step.execution_time:.2f} saniye)')
            
            return JsonResponse({
                'success': True,
                'step_id': str(step.id),
                'message': 'Model başarıyla ovalleştirildi ve kaydedildi',
                'redirect_url': f'/processing/{model.id}/'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return render(request, 'processing/ovalize.html', {'model': model})


def drill_hole(request, model_id):
    """Delik delme"""
    model = get_object_or_404(Model3D, id=model_id)
    
    if request.method == 'POST':
        try:
            from .services import ModelProcessor
            import time
            import os
            from django.core.files import File
            
            # Parametreleri al
            data = json.loads(request.body)
            diameter = float(data.get('diameter', 2.0))
            depth = float(data.get('depth', 5.0))
            position = data.get('position', 'center')
            hole_type = data.get('hole_type', 'through')
            count = int(data.get('count', 1))
            
            # İşleme başlama zamanı
            start_time = time.time()
            
            # Model işlemcisini başlat
            processor = ModelProcessor(model.original_file.path)
            
            # Delik delme işlemini uygula
            success = processor.drill_hole(
                diameter=diameter,
                depth=depth,
                position=position,
                hole_type=hole_type,
                count=count
            )
            
            if not success:
                return JsonResponse({
                    'success': False,
                    'error': 'Delik delme işlemi başarısız oldu'
                }, status=400)
            
            # İşlenmiş modeli kaydet
            temp_path = processor.save_stl()
            
            # ProcessingStep oluştur
            step = ProcessingStep.objects.create(
                model=model,
                step_type='drilling',
                parameters={
                    'diameter': diameter,
                    'depth': depth,
                    'position': position,
                    'hole_type': hole_type,
                    'count': count
                },
                execution_time=time.time() - start_time,
                success=True
            )
            
            # Dosyayı ProcessingStep'e kaydet
            with open(temp_path, 'rb') as f:
                step.result_file.save(
                    f'drill_{model.id}_{step.id}.stl',
                    File(f),
                    save=True
                )
            
            # Temp dosyayı sil
            os.unlink(temp_path)
            
            # Orijinal model dosyasını güncelle
            with open(step.result_file.path, 'rb') as f:
                model.original_file.save(
                    model.original_file.name,
                    File(f),
                    save=True
                )
            
            messages.success(request, f'Delik delme işlemi başarıyla tamamlandı! ({step.execution_time:.2f} saniye)')
            
            return JsonResponse({
                'success': True,
                'step_id': str(step.id),
                'message': 'Delikler başarıyla delindi ve kaydedildi',
                'redirect_url': f'/processing/{model.id}/'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return render(request, 'processing/drill.html', {'model': model})


@require_POST
def save_processing_step(request, model_id):
    """İşlem adımını kaydet (API endpoint)"""
    try:
        model = get_object_or_404(Model3D, id=model_id)
        data = json.loads(request.body)
        
        step_type = data.get('step_type')
        parameters = data.get('parameters', {})
        
        # ProcessingStep oluştur (şimdilik dosya olmadan)
        step = ProcessingStep.objects.create(
            model=model,
            step_type=step_type,
            parameters=parameters,
            execution_time=0.0,  # Backend'de gerçek süre hesaplanacak
            success=True
        )
        
        messages.success(request, f'{step.get_step_type_display()} işlemi kaydedildi!')
        
        return JsonResponse({
            'success': True,
            'step_id': str(step.id),
            'message': 'İşlem başarıyla kaydedildi'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


def complete_processing(request, model_id):
    """İşlemleri tamamla ve sonraki aşamaya geç"""
    model = get_object_or_404(Model3D, id=model_id)
    model.is_processed = True
    model.save()
    
    messages.success(request, 'İşleme aşaması tamamlandı! Artık modeli görselleştirebilir veya indirebilirsiniz.')
    return redirect('models:model_detail', model_id=model.id)
