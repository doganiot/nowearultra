# NoWearUltra - Hızlı Başlangıç

## 🚀 5 Dakikada Başlayın!

### 1. Kurulum (2 dakika)

```bash
# Virtual environment oluştur
python -m venv venv

# Aktive et (Windows)
venv\Scripts\activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# Veritabanını hazırla
python manage.py migrate
```

### 2. Sunucuyu Başlat (30 saniye)

```bash
python manage.py runserver 8002
```

Tarayıcıda aç: **http://localhost:8002/**

### 3. İlk Modelinizi Yükleyin (2 dakika)

1. Ana sayfada **"Model Yükle"** butonuna tıklayın
2. `.stl` veya `.ply` dosyanızı seçin
3. Model adını girin
4. **"Yükle ve Analiz Et"** butonuna tıklayın

### 4. Analiz Sonuçlarını Görüntüleyin

- Vertex ve face sayıları
- Topoloji durumu
- Geometrik özellikler
- 3D görselleştirme

### 5. Model İşleme

- **Döndürme**: Modeli yönlendirin
- **Yumuşatma**: Yüzeyi düzeltin
- **Delik Delme**: Hortum ve vent delikleri
- **Export**: STL/PLY indirin

## 📦 Proje Özellikleri

### ✅ Aşama 1: Model Analizi (Tamamlandı)
- [x] Model yükleme (.stl, .ply)
- [x] Geometrik analiz
- [x] Özellik tespiti
- [x] 3D görselleştirme
- [x] Veritabanı kaydı

### 🔄 Aşama 2: Model İşleme (Devam Ediyor)
- [ ] Döndürme
- [ ] Kesme
- [ ] Delik doldurma
- [ ] Yumuşatma
- [ ] Ovalleştirme
- [ ] Bombeleştirme
- [ ] Delik delme

### ⏳ Aşama 3: Export (Planlı)
- [ ] STL/PLY export
- [ ] Kalite kontrolü
- [ ] İşlem geçmişi

## 🛠️ Teknolojiler

- **Backend**: Django 4.2
- **3D İşleme**: Trimesh, NumPy
- **Görselleştirme**: Plotly
- **Frontend**: Bootstrap 5
- **API**: Django REST Framework

## 📚 Dokümantasyon

- [README.md](README.md) - Genel bakış
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - Mimari tasarım
- [docs/API_DOCS.md](docs/API_DOCS.md) - API dokümantasyonu
- [docs/USER_GUIDE.md](docs/USER_GUIDE.md) - Kullanım kılavuzu
- [docs/DEVELOPER_GUIDE.md](docs/DEVELOPER_GUIDE.md) - Geliştirici kılavuzu

## 🎯 Sonraki Adımlar

1. **Admin Panel**: `/admin` adresinden yönetim paneline erişin
2. **API Explorer**: `/api` adresinden REST API'yi keşfedin
3. **Özelleştirme**: Kendi işleme algoritmalarınızı ekleyin

## 📞 Destek

Sorularınız için: alidoganbektas@gmail.com

---

**Başarılar! 🎉**


