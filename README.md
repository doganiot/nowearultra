# NoWearUltra - 3D Kulak Kalıbı Modelleme Platformu

## 📋 Proje Hakkında

NoWearUltra, kulak kalıplarının 3D modellerini profesyonel, basılabilir kalıplara dönüştüren gelişmiş bir web uygulamasıdır. Kullanıcılar ham tarama verilerini yükleyebilir, modeli analiz edebilir, çeşitli işlemler uygulayabilir ve 3D yazıcıya hazır dosyalar indirebilir.

## 🎯 Ana Özellikler

### 1. Aşama: Model Analizi ve Görselleştirme
- ✅ 3D model yükleme (.stl, .ply)
- ✅ İnteraktif 3D görselleştirme
- ✅ Model özellikleri analizi:
  - Uç noktaları tespiti
  - Alt ve üst noktaları belirleme
  - Sivri bölgeleri tespit etme
  - En geniş alanı bulma
  - Topoloji kontrolü
  - En dar alanı tespit etme

### 2. Aşama: Model İşleme Araçları
- 🔄 Döndürme ve yönlendirme
- ✂️ Kesme ve kırpma
- 🔧 Delik doldurma ve katı hale getirme
- 🎨 Yumuşatma (2 aşamalı)
- 🔘 Kulak kepçe içi ovalleştirme
- 💎 Kulak kanalı ucu bombeleştirme
- 🎯 Hassas delik delme:
  - Hortum deliği (Ø 1.6mm)
  - Vent açıklığı (Ø 0.9mm)

### 3. Aşama: Export ve Kayıt
- 💾 İşlenmiş modeli indirme
- 📊 Tüm detaylarla veritabanı kaydı
- 📈 İşlem geçmişi ve versiyon kontrolü

## 🛠️ Teknoloji Yığını

- **Backend**: Django 4.2.23
- **3D İşleme**: Trimesh, Open3D, NumPy, SciPy
- **Görselleştirme**: Plotly, Three.js (frontend)
- **API**: Django REST Framework
- **Frontend**: Bootstrap 5, jQuery
- **Veritabanı**: SQLite (geliştirme), PostgreSQL (production)

## 📦 Kurulum

### Gereksinimler
- Python 3.13+
- pip
- virtualenv (önerilen)

### Adımlar

1. **Projeyi klonlayın**
```bash
git clone <repository-url>
cd nowearultra
```

2. **Virtual environment oluşturun**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Bağımlılıkları yükleyin**
```bash
pip install -r requirements.txt
```

4. **Veritabanını oluşturun**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Superuser oluşturun**
```bash
python manage.py createsuperuser
```

6. **Geliştirme sunucusunu başlatın**
```bash
python manage.py runserver 8002
```

7. **Tarayıcıda açın**
```
http://localhost:8002/
```

## 📚 Dokümantasyon

Detaylı dokümantasyon için:
- [Mimari Tasarım](docs/ARCHITECTURE.md)
- [API Dokümantasyonu](docs/API_DOCS.md)
- [Kullanım Kılavuzu](docs/USER_GUIDE.md)
- [Geliştirici Kılavuzu](docs/DEVELOPER_GUIDE.md)

## 🔧 Geliştirme Aşamaları

Proje şu anda **Aşama 1** geliştirme sürecindedir.

- [x] Proje yapısı oluşturuldu
- [x] Temel Django konfigürasyonu
- [ ] Model yükleme ve analiz sistemi
- [ ] İnteraktif görselleştirme
- [ ] Model işleme araçları
- [ ] Export ve veritabanı sistemi

## 🤝 Katkıda Bulunma

Bu proje aktif geliştirme aşamasındadır. Katkılarınızı bekliyoruz!

## 📄 Lisans

Bu proje özel kullanım içindir.

## 📞 İletişim

Sorularınız için: [alidoganbektas@gmail.com]

---

**Not**: Bu sistem profesyonel kulak kalıbı üretimi için tasarlanmıştır. Tıbbi cihaz üretiminde yerel yönetmeliklere uygunluğu kontrol ediniz.

