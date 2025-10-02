"""
3D Model ve işleme modelleri
"""
import uuid
import os
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class Project(models.Model):
    """Proje modeli - Kullanıcı projeleri"""
    STATUS_CHOICES = [
        ('draft', 'Taslak'),
        ('processing', 'İşleniyor'),
        ('completed', 'Tamamlandı'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=255, verbose_name='Proje Adı')
    description = models.TextField(blank=True, verbose_name='Açıklama')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Proje'
        verbose_name_plural = 'Projeler'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


def upload_to_original(instance, filename):
    """Original dosyalar için upload path"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('uploads', filename)


class Model3D(models.Model):
    """3D Model dosyası"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='models', null=True, blank=True)
    name = models.CharField(max_length=255, verbose_name='Model Adı')
    original_file = models.FileField(
        upload_to=upload_to_original,
        validators=[FileExtensionValidator(allowed_extensions=['stl', 'ply'])],
        verbose_name='Model Dosyası'
    )
    file_format = models.CharField(max_length=10, verbose_name='Dosya Formatı')
    file_size = models.BigIntegerField(verbose_name='Dosya Boyutu (bytes)')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False, verbose_name='İşlendi mi?')
    
    class Meta:
        verbose_name = '3D Model'
        verbose_name_plural = '3D Modeller'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.original_file:
            # Dosya formatını otomatik belirle
            self.file_format = self.original_file.name.split('.')[-1].lower()
            # Dosya boyutunu kaydet
            self.file_size = self.original_file.size
        super().save(*args, **kwargs)


class ModelAnalysis(models.Model):
    """Model analiz sonuçları"""
    TOPOLOGY_CHOICES = [
        ('good', 'İyi'),
        ('has_holes', 'Delikli'),
        ('non_manifold', 'Manifold Değil'),
        ('complex', 'Karmaşık'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    model = models.OneToOneField(Model3D, on_delete=models.CASCADE, related_name='analysis')
    
    # Geometri bilgileri
    vertices_count = models.IntegerField(verbose_name='Vertex Sayısı')
    faces_count = models.IntegerField(verbose_name='Face Sayısı')
    is_watertight = models.BooleanField(default=False, verbose_name='Kapalı mı?')
    volume = models.FloatField(null=True, blank=True, verbose_name='Hacim (mm³)')
    surface_area = models.FloatField(null=True, blank=True, verbose_name='Yüzey Alanı (mm²)')
    
    # Bounding box
    bounding_box_min = models.JSONField(verbose_name='Bounding Box Min')
    bounding_box_max = models.JSONField(verbose_name='Bounding Box Max')
    
    # Feature points
    top_points = models.JSONField(verbose_name='Üst Noktalar')
    bottom_points = models.JSONField(verbose_name='Alt Noktalar')
    sharp_points = models.JSONField(verbose_name='Sivri Noktalar')
    
    # Dimensions
    widest_area = models.JSONField(verbose_name='En Geniş Alan')
    narrowest_area = models.JSONField(verbose_name='En Dar Alan')
    
    # Topology
    topology_status = models.CharField(max_length=20, choices=TOPOLOGY_CHOICES, verbose_name='Topoloji Durumu')
    
    analyzed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Model Analizi'
        verbose_name_plural = 'Model Analizleri'
    
    def __str__(self):
        return f"Analiz: {self.model.name}"


def upload_to_processed(instance, filename):
    """Processed dosyalar için upload path"""
    ext = filename.split('.')[-1]
    filename = f"step_{instance.step_type}_{uuid.uuid4()}.{ext}"
    return os.path.join('processed', filename)


class ProcessingStep(models.Model):
    """İşleme adımı kaydı"""
    STEP_TYPES = [
        ('rotation', 'Döndürme'),
        ('cutting', 'Kesme'),
        ('fill_holes', 'Delik Doldurma'),
        ('smoothing', 'Yumuşatma'),
        ('ovalization', 'Ovalleştirme'),
        ('bulging', 'Bombeleştirme'),
        ('drilling', 'Delik Delme'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    model = models.ForeignKey(Model3D, on_delete=models.CASCADE, related_name='processing_steps')
    step_type = models.CharField(max_length=20, choices=STEP_TYPES, verbose_name='İşlem Tipi')
    parameters = models.JSONField(verbose_name='Parametreler')
    result_file = models.FileField(
        upload_to=upload_to_processed,
        validators=[FileExtensionValidator(allowed_extensions=['stl', 'ply'])],
        verbose_name='Sonuç Dosyası',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    execution_time = models.FloatField(verbose_name='Çalışma Süresi (saniye)')
    success = models.BooleanField(default=True, verbose_name='Başarılı mı?')
    error_message = models.TextField(blank=True, verbose_name='Hata Mesajı')
    
    class Meta:
        verbose_name = 'İşleme Adımı'
        verbose_name_plural = 'İşleme Adımları'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_step_type_display()} - {self.model.name}"


def upload_to_exports(instance, filename):
    """Export dosyalar için upload path"""
    return os.path.join('exports', filename)


class ProcessedModel(models.Model):
    """İşlenmiş final model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_model = models.ForeignKey(Model3D, on_delete=models.CASCADE, related_name='processed_versions')
    processed_file = models.FileField(
        upload_to=upload_to_exports,
        validators=[FileExtensionValidator(allowed_extensions=['stl', 'ply'])],
        verbose_name='İşlenmiş Dosya'
    )
    processing_steps = models.ManyToManyField(ProcessingStep, verbose_name='İşleme Adımları')
    
    # Final model stats
    final_vertices_count = models.IntegerField(verbose_name='Final Vertex Sayısı')
    final_faces_count = models.IntegerField(verbose_name='Final Face Sayısı')
    quality_score = models.FloatField(null=True, blank=True, verbose_name='Kalite Skoru')
    is_printable = models.BooleanField(default=False, verbose_name='Basılabilir mi?')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'İşlenmiş Model'
        verbose_name_plural = 'İşlenmiş Modeller'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"İşlenmiş: {self.original_model.name}"
