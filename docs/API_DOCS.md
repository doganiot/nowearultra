# NoWearUltra - API Dokümantasyonu

## 📡 API Genel Bakış

NoWearUltra REST API, 3D kulak kalıbı modellerinin yüklenmesi, analiz edilmesi, işlenmesi ve export edilmesi için endpoint'ler sağlar.

**Base URL**: `http://localhost:8002/api/v1/`

**Yetkilendirme**: Session-based authentication (Django)

## 📋 İçindekiler

1. [Model İşlemleri](#model-işlemleri)
2. [Analiz İşlemleri](#analiz-işlemleri)
3. [İşleme İşlemleri](#işleme-işlemleri)
4. [Görselleştirme](#görselleştirme)
5. [Export İşlemleri](#export-işlemleri)
6. [Hata Kodları](#hata-kodları)

---

## Model İşlemleri

### 1. Model Yükleme

**Endpoint**: `POST /api/v1/models/upload/`

**Açıklama**: Yeni bir 3D model yükler ve analiz başlatır.

**Request**:
```http
POST /api/v1/models/upload/
Content-Type: multipart/form-data

{
  "file": <binary>,
  "name": "string",
  "project_id": "uuid (optional)",
  "description": "string (optional)"
}
```

**Response** (201 Created):
```json
{
  "id": "uuid",
  "name": "model_name",
  "file_format": "stl",
  "file_size": 1234567,
  "uploaded_at": "2025-10-02T10:30:00Z",
  "status": "analyzing",
  "message": "Model başarıyla yüklendi ve analiz ediliyor"
}
```

**Örnek (cURL)**:
```bash
curl -X POST http://localhost:8002/api/v1/models/upload/ \
  -H "Content-Type: multipart/form-data" \
  -F "file=@ear_scan.stl" \
  -F "name=Kulak Taraması 001"
```

---

### 2. Model Detayı

**Endpoint**: `GET /api/v1/models/{model_id}/`

**Response** (200 OK):
```json
{
  "id": "uuid",
  "name": "model_name",
  "file_format": "stl",
  "file_size": 1234567,
  "uploaded_at": "2025-10-02T10:30:00Z",
  "is_processed": false,
  "project": {
    "id": "uuid",
    "name": "project_name"
  },
  "file_url": "/media/uploads/model.stl"
}
```

---

### 3. Model Listesi

**Endpoint**: `GET /api/v1/models/`

**Query Parameters**:
- `project_id`: UUID (filter by project)
- `is_processed`: boolean
- `ordering`: string (created_at, -created_at, name)
- `page`: integer
- `page_size`: integer

**Response** (200 OK):
```json
{
  "count": 10,
  "next": "url_to_next_page",
  "previous": null,
  "results": [
    {
      "id": "uuid",
      "name": "model_name",
      "uploaded_at": "2025-10-02T10:30:00Z",
      "is_processed": false
    }
  ]
}
```

---

### 4. Model Silme

**Endpoint**: `DELETE /api/v1/models/{model_id}/`

**Response** (204 No Content)

---

## Analiz İşlemleri

### 1. Model Analizi Görüntüleme

**Endpoint**: `GET /api/v1/models/{model_id}/analysis/`

**Response** (200 OK):
```json
{
  "id": "uuid",
  "model_id": "uuid",
  "analyzed_at": "2025-10-02T10:35:00Z",
  "geometry": {
    "vertices_count": 15234,
    "faces_count": 30468,
    "is_watertight": true,
    "volume": 3456.78,
    "surface_area": 2345.67
  },
  "bounding_box": {
    "min": [-10.5, -8.3, -12.1],
    "max": [10.5, 8.3, 12.1],
    "dimensions": [21.0, 16.6, 24.2]
  },
  "feature_points": {
    "top_points": [
      {"x": 0, "y": 8.3, "z": 0},
      {"x": 1.2, "y": 7.9, "z": 0.5}
    ],
    "bottom_points": [
      {"x": 0, "y": -8.3, "z": 0},
      {"x": -1.1, "y": -8.1, "z": -0.3}
    ],
    "sharp_points": [
      {"x": 5.2, "y": 3.1, "z": 4.5, "curvature": 0.92}
    ]
  },
  "dimensions": {
    "widest_area": {
      "position": {"x": 0, "y": 2.1, "z": 0},
      "width": 18.5,
      "direction": "x"
    },
    "narrowest_area": {
      "position": {"x": 0, "y": -5.2, "z": 3.1},
      "width": 4.2,
      "direction": "y"
    }
  },
  "topology": {
    "status": "good",
    "issues": [],
    "euler_characteristic": 2,
    "genus": 0,
    "connected_components": 1
  }
}
```

---

### 2. Analiz Yenileme

**Endpoint**: `POST /api/v1/models/{model_id}/reanalyze/`

**Response** (202 Accepted):
```json
{
  "message": "Analiz başlatıldı",
  "task_id": "uuid"
}
```

---

## İşleme İşlemleri

### 1. Model Döndürme

**Endpoint**: `POST /api/v1/processing/rotate/`

**Request**:
```json
{
  "model_id": "uuid",
  "axis": "z",
  "angle": 90,
  "center": [0, 0, 0]
}
```

**Response** (200 OK):
```json
{
  "step_id": "uuid",
  "model_id": "uuid",
  "step_type": "rotation",
  "parameters": {
    "axis": "z",
    "angle": 90
  },
  "result_file": "/media/processed/model_rotated.stl",
  "preview_url": "/api/v1/visualization/uuid/preview/",
  "execution_time": 0.234,
  "success": true
}
```

---

### 2. Model Kesme

**Endpoint**: `POST /api/v1/processing/cut/`

**Request**:
```json
{
  "model_id": "uuid",
  "plane_origin": [0, 0, 5],
  "plane_normal": [0, 0, 1],
  "keep_side": "positive"
}
```

**Response** (200 OK):
```json
{
  "step_id": "uuid",
  "result_file": "/media/processed/model_cut.stl",
  "execution_time": 0.456
}
```

---

### 3. Delik Doldurma

**Endpoint**: `POST /api/v1/processing/fill-holes/`

**Request**:
```json
{
  "model_id": "uuid",
  "max_hole_size": 100
}
```

**Response** (200 OK):
```json
{
  "step_id": "uuid",
  "holes_filled": 5,
  "result_file": "/media/processed/model_filled.stl"
}
```

---

### 4. Yumuşatma

**Endpoint**: `POST /api/v1/processing/smooth/`

**Request**:
```json
{
  "model_id": "uuid",
  "iterations": 10,
  "lambda_factor": 0.5,
  "method": "laplacian"
}
```

**Response** (200 OK):
```json
{
  "step_id": "uuid",
  "result_file": "/media/processed/model_smoothed.stl"
}
```

---

### 5. Ovalleştirme (Kulak Kepçe İçi)

**Endpoint**: `POST /api/v1/processing/ovalize/`

**Request**:
```json
{
  "model_id": "uuid",
  "region": {
    "center": [0, 2, 0],
    "radius": 5
  },
  "intensity": 0.7
}
```

---

### 6. Bombeleştirme (Kulak Kanalı Ucu)

**Endpoint**: `POST /api/v1/processing/bulge/`

**Request**:
```json
{
  "model_id": "uuid",
  "region": {
    "center": [0, -5, 3],
    "radius": 3
  },
  "intensity": 0.5
}
```

---

### 7. Delik Delme

**Endpoint**: `POST /api/v1/processing/drill/`

**Request**:
```json
{
  "model_id": "uuid",
  "holes": [
    {
      "name": "hortum_deligi",
      "position": [2, 0, 1],
      "direction": [0, 0, 1],
      "diameter": 1.7,
      "depth": 10
    },
    {
      "name": "vent_acikligi",
      "position": [-2, 0, 1],
      "direction": [0, 0, 1],
      "diameter": 0.9,
      "depth": 8
    }
  ]
}
```

**Response** (200 OK):
```json
{
  "step_id": "uuid",
  "holes_drilled": 2,
  "result_file": "/media/processed/model_drilled.stl",
  "holes": [
    {
      "name": "hortum_deligi",
      "success": true,
      "actual_position": [2, 0, 1]
    },
    {
      "name": "vent_acikligi",
      "success": true,
      "actual_position": [-2, 0, 1]
    }
  ]
}
```

---

### 8. İşlem Geçmişi

**Endpoint**: `GET /api/v1/processing/steps/{model_id}/`

**Response** (200 OK):
```json
{
  "model_id": "uuid",
  "steps": [
    {
      "step_id": "uuid",
      "step_type": "rotation",
      "created_at": "2025-10-02T11:00:00Z",
      "parameters": {},
      "success": true
    }
  ]
}
```

---

### 9. İşlemi Geri Al

**Endpoint**: `POST /api/v1/processing/undo/`

**Request**:
```json
{
  "model_id": "uuid",
  "step_id": "uuid"
}
```

---

## Görselleştirme

### 1. 3D Render

**Endpoint**: `GET /api/v1/visualization/{model_id}/render/`

**Query Parameters**:
- `format`: string (json, html)
- `width`: integer (default: 800)
- `height`: integer (default: 600)

**Response** (200 OK):
```json
{
  "model_id": "uuid",
  "render_data": {
    "vertices": [[x, y, z], ...],
    "faces": [[i, j, k], ...],
    "normals": [[nx, ny, nz], ...],
    "colors": [[r, g, b], ...]
  },
  "camera": {
    "position": [0, 0, 50],
    "target": [0, 0, 0]
  }
}
```

---

### 2. Önizleme İmajı

**Endpoint**: `GET /api/v1/visualization/{model_id}/preview/`

**Response**: PNG image

---

## Export İşlemleri

### 1. Model Export

**Endpoint**: `POST /api/v1/export/{model_id}/`

**Request**:
```json
{
  "format": "stl",
  "binary": true,
  "include_metadata": true
}
```

**Response** (200 OK):
```json
{
  "export_id": "uuid",
  "download_url": "/api/v1/export/uuid/download/",
  "file_size": 2345678,
  "expires_at": "2025-10-03T10:00:00Z"
}
```

---

### 2. Dosya İndirme

**Endpoint**: `GET /api/v1/export/{export_id}/download/`

**Response**: Binary file (STL/PLY)

---

## Hata Kodları

### Genel Hatalar

```json
{
  "error": "error_code",
  "message": "Human-readable error message",
  "details": {}
}
```

### HTTP Durum Kodları

- `200 OK` - Başarılı istek
- `201 Created` - Kaynak oluşturuldu
- `202 Accepted` - İşlem kuyruğa alındı
- `204 No Content` - Başarılı silme
- `400 Bad Request` - Geçersiz istek
- `401 Unauthorized` - Yetkilendirme gerekli
- `403 Forbidden` - Erişim reddedildi
- `404 Not Found` - Kaynak bulunamadı
- `413 Payload Too Large` - Dosya çok büyük
- `415 Unsupported Media Type` - Geçersiz dosya formatı
- `422 Unprocessable Entity` - İşlem hatası
- `500 Internal Server Error` - Sunucu hatası

### Özel Hata Kodları

- `MODEL_INVALID` - Model dosyası geçersiz
- `MODEL_NOT_WATERTIGHT` - Model kapalı değil
- `ANALYSIS_FAILED` - Analiz başarısız
- `PROCESSING_FAILED` - İşlem başarısız
- `FILE_TOO_LARGE` - Dosya 50MB'dan büyük
- `UNSUPPORTED_FORMAT` - Desteklenmeyen format
- `INSUFFICIENT_GEOMETRY` - Yetersiz geometri
- `TOPOLOGY_ERROR` - Topoloji hatası

---

## Rate Limiting

API rate limiting uygulanmaktadır:
- **Anonim kullanıcılar**: 20 istek/saat
- **Kayıtlı kullanıcılar**: 100 istek/saat
- **Premium kullanıcılar**: 500 istek/saat

Rate limit aşıldığında `429 Too Many Requests` döner:

```json
{
  "error": "rate_limit_exceeded",
  "message": "Çok fazla istek gönderdiniz",
  "retry_after": 3600
}
```

---

## Örnek İş Akışı

```javascript
// 1. Model yükle
const uploadResponse = await fetch('/api/v1/models/upload/', {
  method: 'POST',
  body: formData
});
const { id: modelId } = await uploadResponse.json();

// 2. Analiz sonuçlarını bekle
const analysis = await fetch(`/api/v1/models/${modelId}/analysis/`);

// 3. Döndürme uygula
await fetch('/api/v1/processing/rotate/', {
  method: 'POST',
  body: JSON.stringify({ model_id: modelId, axis: 'z', angle: 90 })
});

// 4. Yumuşatma uygula
await fetch('/api/v1/processing/smooth/', {
  method: 'POST',
  body: JSON.stringify({ model_id: modelId, iterations: 10 })
});

// 5. Export et
const exportResponse = await fetch(`/api/v1/export/${modelId}/`, {
  method: 'POST',
  body: JSON.stringify({ format: 'stl', binary: true })
});
const { download_url } = await exportResponse.json();

// 6. İndir
window.location.href = download_url;
```

---

**Son Güncelleme**: 2025-10-02


