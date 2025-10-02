# NoWearUltra - Mimari Tasarım Dokümantasyonu

## 🏗️ Sistem Mimarisi

NoWearUltra, modüler ve ölçeklenebilir bir mimari ile tasarlanmıştır.

## 📐 Genel Yapı

```
┌─────────────────────────────────────────────────────────┐
│                     Web Browser                         │
│  (React/jQuery + Three.js + Bootstrap 5)               │
└──────────────────┬──────────────────────────────────────┘
                   │ HTTP/REST API
┌──────────────────▼──────────────────────────────────────┐
│                Django Application                        │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │   Upload    │  │   Analysis   │  │  Processing   │  │
│  │   Module    │  │    Module    │  │    Module     │  │
│  └─────────────┘  └──────────────┘  └───────────────┘  │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │Visualization│  │   Database   │  │    Export     │  │
│  │   Module    │  │    Module    │  │    Module     │  │
│  └─────────────┘  └──────────────┘  └───────────────┘  │
└─────────────────────────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│           3D Processing Libraries                        │
│   (Trimesh, Open3D, NumPy, SciPy, NetworkX)            │
└─────────────────────────────────────────────────────────┘
```

## 🗂️ Dizin Yapısı

```
nowearultra/
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── config/                      # Django proje ayarları
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/
│   ├── core/                    # Temel uygulama (anasayfa, genel)
│   │   ├── migrations/
│   │   ├── templates/
│   │   ├── static/
│   │   ├── models.py
│   │   ├── views.py
│   │   └── urls.py
│   │
│   ├── models/                  # 3D model yönetimi
│   │   ├── migrations/
│   │   ├── models.py           # Model, Project, ProcessingHistory
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── forms.py
│   │   └── urls.py
│   │
│   ├── analysis/                # Model analiz modülü (Aşama 1)
│   │   ├── services/
│   │   │   ├── feature_detector.py    # Özellik tespiti
│   │   │   ├── topology_analyzer.py   # Topoloji analizi
│   │   │   └── geometry_utils.py      # Geometri yardımcıları
│   │   ├── models.py
│   │   ├── views.py
│   │   └── urls.py
│   │
│   ├── processing/              # Model işleme modülü (Aşama 2)
│   │   ├── services/
│   │   │   ├── rotation.py            # Döndürme
│   │   │   ├── cutting.py             # Kesme
│   │   │   ├── hole_filling.py        # Delik doldurma
│   │   │   ├── smoothing.py           # Yumuşatma
│   │   │   ├── ovalization.py         # Ovalleştirme
│   │   │   ├── bulging.py             # Bombeleştirme
│   │   │   └── drilling.py            # Delik delme
│   │   ├── models.py
│   │   ├── views.py
│   │   └── urls.py
│   │
│   ├── visualization/           # 3D görselleştirme
│   │   ├── services/
│   │   │   ├── renderer.py
│   │   │   └── exporter.py
│   │   ├── views.py
│   │   └── urls.py
│   │
│   └── api/                     # REST API endpoints
│       ├── v1/
│       │   ├── serializers.py
│       │   ├── views.py
│       │   └── urls.py
│       └── urls.py
│
├── media/                       # Kullanıcı yüklenen dosyalar
│   ├── uploads/                # Ham model dosyaları
│   ├── processed/              # İşlenmiş modeller
│   └── exports/                # Export edilen dosyalar
│
├── static/                      # Statik dosyalar
│   ├── css/
│   ├── js/
│   │   ├── three.min.js
│   │   └── model_viewer.js
│   └── images/
│
├── templates/                   # HTML şablonlar
│   ├── base.html
│   ├── index.html
│   └── includes/
│
└── docs/                        # Dokümantasyon
    ├── ARCHITECTURE.md
    ├── API_DOCS.md
    ├── USER_GUIDE.md
    └── DEVELOPER_GUIDE.md
```

## 💾 Veritabanı Şeması

### Model Tabloları

#### Project (Proje)
```python
- id: UUID (PK)
- user: ForeignKey(User)
- name: CharField
- description: TextField
- created_at: DateTimeField
- updated_at: DateTimeField
- status: CharField (draft, processing, completed)
```

#### Model3D (3D Model)
```python
- id: UUID (PK)
- project: ForeignKey(Project)
- name: CharField
- original_file: FileField
- file_format: CharField (stl, ply)
- file_size: BigIntegerField
- uploaded_at: DateTimeField
- is_processed: BooleanField
```

#### ModelAnalysis (Model Analizi)
```python
- id: UUID (PK)
- model: OneToOneField(Model3D)
- vertices_count: IntegerField
- faces_count: IntegerField
- is_watertight: BooleanField
- volume: FloatField
- surface_area: FloatField
- bounding_box_min: JSONField
- bounding_box_max: JSONField
- top_points: JSONField
- bottom_points: JSONField
- sharp_points: JSONField
- widest_area: JSONField
- narrowest_area: JSONField
- topology_status: CharField
- analyzed_at: DateTimeField
```

#### ProcessingStep (İşleme Adımı)
```python
- id: UUID (PK)
- model: ForeignKey(Model3D)
- step_type: CharField (rotation, cutting, smoothing, etc.)
- parameters: JSONField
- result_file: FileField
- created_at: DateTimeField
- execution_time: FloatField
- success: BooleanField
- error_message: TextField
```

#### ProcessedModel (İşlenmiş Model)
```python
- id: UUID (PK)
- original_model: ForeignKey(Model3D)
- processed_file: FileField
- processing_steps: ManyToManyField(ProcessingStep)
- final_vertices_count: IntegerField
- final_faces_count: IntegerField
- quality_score: FloatField
- is_printable: BooleanField
- created_at: DateTimeField
```

## 🔄 İşlem Akışı

### Aşama 1: Model Yükleme ve Analiz

```
1. Kullanıcı model yükler (.stl/.ply)
   ↓
2. Dosya validasyonu ve kayıt
   ↓
3. Model3D nesnesi oluşturulur
   ↓
4. Trimesh ile model yüklenir
   ↓
5. Geometrik analiz başlatılır:
   - Vertex/face sayısı
   - Bounding box hesaplama
   - Uç noktaları tespit
   - Sivri noktaları tespit
   - Geniş/dar alanları bul
   - Topoloji kontrolü
   ↓
6. ModelAnalysis kaydı oluşturulur
   ↓
7. 3D görselleştirme hazırlanır
   ↓
8. Sonuçlar kullanıcıya gösterilir
```

### Aşama 2: Model İşleme

```
Kullanıcı işlem seçer
   ↓
İşlem parametreleri alınır
   ↓
ProcessingService çağrılır
   ↓
İşlem uygulanır (Trimesh/Open3D)
   ↓
Sonuç kaydedilir
   ↓
ProcessingStep oluşturulur
   ↓
Önizleme gösterilir
   ↓
Kullanıcı onayla/iptal eder
```

### Aşama 3: Export

```
Kullanıcı export ister
   ↓
ProcessedModel oluşturulur
   ↓
Kalite kontrolü yapılır
   ↓
Dosya export edilir (.stl/.ply)
   ↓
İndirme linki sunulur
   ↓
Veritabanına tam kayıt
```

## 🔌 API Endpoints

### Model İşlemleri
- `POST /api/v1/models/upload/` - Model yükleme
- `GET /api/v1/models/{id}/` - Model detayı
- `GET /api/v1/models/{id}/analysis/` - Analiz sonuçları
- `DELETE /api/v1/models/{id}/` - Model silme

### İşleme İşlemleri
- `POST /api/v1/processing/rotate/` - Döndürme
- `POST /api/v1/processing/cut/` - Kesme
- `POST /api/v1/processing/fill-holes/` - Delik doldurma
- `POST /api/v1/processing/smooth/` - Yumuşatma
- `POST /api/v1/processing/ovalize/` - Ovalleştirme
- `POST /api/v1/processing/bulge/` - Bombeleştirme
- `POST /api/v1/processing/drill/` - Delik delme

### Görselleştirme
- `GET /api/v1/visualization/{id}/render/` - 3D render
- `GET /api/v1/visualization/{id}/preview/` - Önizleme

### Export
- `POST /api/v1/export/{id}/` - Model export
- `GET /api/v1/export/{id}/download/` - Dosya indirme

## 🔐 Güvenlik

- CSRF koruması aktif
- Dosya tipi validasyonu
- Dosya boyutu limiti (max 50MB)
- Kullanıcı yetkilendirmesi
- Rate limiting (API)

## 📊 Performans Optimizasyonu

- Asenkron dosya işleme (Celery - gelecek)
- Model önbellekleme (Redis - gelecek)
- CDN entegrasyonu (statik dosyalar)
- Veritabanı indeksleme
- Lazy loading (3D görselleştirme)

## 🧪 Test Stratejisi

- Unit testler (her modül)
- Integration testler (API)
- 3D işleme doğrulama testleri
- UI testleri (Selenium)
- Performance testleri

## 🚀 Deployment

- Docker containerization
- Nginx reverse proxy
- PostgreSQL (production DB)
- Static dosyalar → S3/CDN
- SSL/HTTPS zorunlu

---

**Son Güncelleme**: 2025-10-02


