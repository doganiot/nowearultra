# NoWearUltra - Geliştirici Kılavuzu

## 🏗️ Proje Yapısı

```
nowearultra/
├── apps/
│   ├── core/              # Ana sayfa ve genel views
│   ├── models/            # 3D model yönetimi
│   ├── analysis/          # Model analiz servisleri
│   │   └── services/
│   │       ├── feature_detector.py    # Özellik tespit
│   │       ├── topology_analyzer.py   # Topoloji analiz
│   │       └── geometry_utils.py      # Geometri yardımcıları
│   ├── processing/        # Model işleme araçları
│   │   └── services/
│   │       ├── rotation.py
│   │       ├── cutting.py
│   │       ├── smoothing.py
│   │       └── drilling.py
│   └── visualization/     # 3D görselleştirme
│
├── config/                # Django ayarları
├── templates/             # HTML şablonlar
├── static/                # Statik dosyalar
├── media/                 # Kullanıcı dosyaları
│   ├── uploads/           # Yüklenen modeller
│   ├── processed/         # İşlenmiş modeller
│   └── exports/           # Export edilen dosyalar
└── docs/                  # Dokümantasyon
```

## 🔧 Geliştirme Ortamı Kurulumu

### Gereksinimler
- Python 3.13+
- pip
- virtualenv
- Git

### Kurulum
```bash
# Repoyu klonla
git clone <repo-url>
cd nowearultra

# Virtual environment oluştur
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# Veritabanını oluştur
python manage.py migrate

# Statik dosyaları topla
python manage.py collectstatic --no-input

# Superuser oluştur
python manage.py createsuperuser

# Geliştirme sunucusunu başlat
python manage.py runserver 8002
```

## 📦 Yeni Özellik Ekleme

### 1. Yeni İşleme Servisi Ekleme

```python
# apps/processing/services/my_operation.py
import trimesh
import numpy as np

class MyOperation:
    def __init__(self, mesh_path):
        self.mesh = trimesh.load(mesh_path)
    
    def process(self, **params):
        # İşleme mantığı
        result_mesh = self.mesh.copy()
        
        # ... işlemler ...
        
        return result_mesh
```

### 2. View Ekleme

```python
# apps/processing/views.py
from .services.my_operation import MyOperation

def my_operation_view(request, model_id):
    model = get_object_or_404(Model3D, id=model_id)
    
    if request.method == 'POST':
        # Parametreleri al
        params = request.POST.dict()
        
        # İşlemi gerçekleştir
        operator = MyOperation(model.original_file.path)
        result_mesh = operator.process(**params)
        
        # Sonucu kaydet
        # ...
        
    return render(request, 'processing/my_operation.html', {'model': model})
```

### 3. URL Pattern Ekleme

```python
# apps/processing/urls.py
urlpatterns = [
    # ... diğer pattern'ler
    path('<uuid:model_id>/my-operation/', views.my_operation_view, name='my_operation'),
]
```

### 4. Template Oluşturma

```html
<!-- templates/processing/my_operation.html -->
{% extends 'base.html' %}

{% block content %}
<form method="post">
    {% csrf_token %}
    <!-- Form alanları -->
    <button type="submit">İşle</button>
</form>
{% endblock %}
```

## 🧪 Test Yazma

### Unit Test
```python
# apps/analysis/tests.py
from django.test import TestCase
from apps.models.models import Model3D
from .services.feature_detector import FeatureDetector

class FeatureDetectorTest(TestCase):
    def setUp(self):
        # Test verileri hazırla
        pass
    
    def test_vertex_count(self):
        detector = FeatureDetector('test_model.stl')
        analysis = detector.analyze()
        self.assertGreater(analysis['vertices_count'], 0)
```

### Integration Test
```python
from django.test import Client

class ModelUploadTest(TestCase):
    def test_upload_stl(self):
        client = Client()
        with open('test_model.stl', 'rb') as f:
            response = client.post('/models/upload/', {
                'file': f,
                'name': 'Test Model'
            })
        self.assertEqual(response.status_code, 302)
```

## 🐛 Debugging

### Django Debug Toolbar
```python
# config/settings.py (development)
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
```

### Logging
```python
# config/settings.py
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    },
}
```

## 📊 Veritabanı İşlemleri

### Migration Oluşturma
```bash
python manage.py makemigrations
python manage.py migrate
```

### Model Değişikliği
```python
# apps/models/models.py
class Model3D(models.Model):
    # Yeni alan ekle
    new_field = models.CharField(max_length=100, default='')
```

### Data Migration
```python
# Generated migration file
def migrate_data(apps, schema_editor):
    Model3D = apps.get_model('models', 'Model3D')
    for model in Model3D.objects.all():
        model.new_field = 'default_value'
        model.save()

class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(migrate_data),
    ]
```

## 🚀 Deployment

### Production Settings
```python
# config/settings_prod.py
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nowearultra',
        # ...
    }
}

# S3 için media dosyaları
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

### Docker
```dockerfile
# Dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## 🔐 Güvenlik

### File Upload Validation
```python
from django.core.validators import FileExtensionValidator

class Model3D(models.Model):
    original_file = models.FileField(
        validators=[
            FileExtensionValidator(['stl', 'ply']),
            validate_file_size,  # Custom validator
        ]
    )

def validate_file_size(value):
    if value.size > 52428800:  # 50MB
        raise ValidationError('Dosya 50MB\'dan büyük olamaz.')
```

### User Permissions
```python
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('models.delete_model3d')
def delete_model(request, model_id):
    # ...
```

## 📝 Kod Standartları

### Python Style Guide
- PEP 8 kurallarına uyun
- Black formatter kullanın
- Type hints ekleyin

```python
def analyze_mesh(mesh_path: str, threshold: float = 0.5) -> Dict[str, Any]:
    """
    Mesh analiz fonksiyonu.
    
    Args:
        mesh_path: Mesh dosya yolu
        threshold: Eşik değeri
        
    Returns:
        Analiz sonuçları dictionary
    """
    pass
```

### Docstring Format
```python
class FeatureDetector:
    """
    3D model özellik tespit sınıfı.
    
    Bu sınıf trimesh kullanarak 3D modellerin geometrik
    özelliklerini tespit eder.
    
    Attributes:
        mesh: Trimesh nesnesi
        file_path: Dosya yolu
        
    Example:
        >>> detector = FeatureDetector('model.stl')
        >>> analysis = detector.analyze()
        >>> print(analysis['vertices_count'])
    """
```

## 🔄 Git Workflow

### Branch Strategy
- `main`: Production
- `develop`: Development
- `feature/xyz`: Yeni özellik
- `bugfix/xyz`: Bug düzeltme

### Commit Messages
```
feat: Add rotation processing service
fix: Fix mesh topology detection
docs: Update API documentation
refactor: Optimize feature detector
test: Add unit tests for analysis
```

## 📚 Faydalı Kaynaklar

### Trimesh Documentation
- [Trimesh Docs](https://trimsh.org/)
- [Mesh Repair](https://github.com/mikedh/trimesh/blob/main/examples/repair.py)

### Django Best Practices
- [Django Documentation](https://docs.djangoproject.com/)
- [Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-3-x)

### 3D Processing
- [Open3D Tutorial](http://www.open3d.org/docs/)
- [Point Cloud Processing](https://github.com/daavoo/pyntcloud)

---

**Son Güncelleme**: 2025-10-02


