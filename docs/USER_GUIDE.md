# NoWearUltra - Kullanım Kılavuzu

## 🚀 Hızlı Başlangıç

### 1. Model Yükleme

1. Ana sayfada veya menüden **"Model Yükle"** butonuna tıklayın
2. Dosyanızı sürükleyip bırakın veya **"Dosya Seç"** butonuna tıklayın
3. Desteklenen formatlar: `.stl` ve `.ply` (Maksimum 50MB)
4. Model adını girin
5. **"Yükle ve Analiz Et"** butonuna tıklayın

### 2. Model Analizi

Model yüklendikten sonra otomatik olarak analiz edilir:

- **Geometrik Bilgiler**: Vertex ve face sayıları
- **Topoloji Kontrolü**: Modelin kapalı (watertight) olup olmadığı
- **Özellik Tespiti**: 
  - Uç noktaları (en üst ve en alt)
  - Sivri noktalar
  - En geniş ve dar alanlar
  - Bounding box boyutları

#### Analiz Sonuçlarını Görüntüleme

1. Model listesinden modelinizi seçin
2. **"Analiz Sonuçları"** butonuna tıklayın
3. Detaylı analiz raporunu inceleyin

### 3. 3D Görselleştirme

1. Model detay sayfasından **"3D Görüntüle"** butonuna tıklayın
2. İnteraktif 3D görüntüleyici ile modelinizi inceleyin
3. Fare ile döndürebilir, yakınlaştırabilirsiniz

### 4. Model İşleme (Aşama 2)

Model işleme panelinden şu işlemleri yapabilirsiniz:

#### 4.1 Döndürme
- X, Y veya Z ekseni etrafında döndürme
- Derece cinsinden açı girişi
- Anlık önizleme

#### 4.2 Kesme
- Düzlem tanımlama (origin ve normal)
- Hangi tarafın tutulacağını seçme
- Kesim önizlemesi

#### 4.3 Delik Doldurma
- Otomatik delik tespit
- Maksimum delik boyutu belirleme
- Katı model oluşturma

#### 4.4 Yumuşatma
- Laplacian veya Taubin yumuşatma
- İterasyon sayısı
- Lambda faktörü
- 2 aşamalı yumuşatma önerilir

#### 4.5 Ovalleştirme (Kulak Kepçe İçi)
- Bölge seçimi (merkez ve yarıçap)
- Yoğunluk ayarı (0-1)
- İçeri doğru şekillendirme

#### 4.6 Bombeleştirme (Kulak Kanalı Ucu)
- Bölge seçimi
- Bombeleştirme yoğunluğu
- Dışarı doğru şişirme

#### 4.7 Delik Delme
- **Hortum Deliği**: Ø 1.7mm
- **Vent Açıklığı**: Ø 0.9mm
- Konum ve derinlik belirtme

### 5. Model Export (Aşama 3)

1. İşleme işlemleri tamamlandıktan sonra **"Export"** butonuna tıklayın
2. Format seçin (STL veya PLY)
3. Binary veya ASCII format seçeneği
4. **"İndir"** butonuna tıklayın
5. 3D yazıcınızda kullanmaya hazır!

## 📊 İpuçları ve En İyi Uygulamalar

### Model Kalitesi
- Yüksek çözünürlüklü taramalar daha iyi sonuç verir
- Modelin kapalı (watertight) olması önerilir
- Gürültülü taramalar için önce yumuşatma uygulayın

### İşleme Sırası
Önerilen işlem sırası:

1. **Döndürme**: Modeli doğru yöne çevirin
2. **Kesme**: Gereksiz kısımları kaldırın
3. **Delik Doldurma**: Topolojiyi düzeltin
4. **1. Yumuşatma**: İlk düzeltme
5. **Ovalleştirme**: Kulak kepçe şekillendirme
6. **Bombeleştirme**: Kanal ucu şekillendirme
7. **2. Yumuşatma**: Final yumuşatma
8. **Delik Delme**: Son aşama

### Performans
- Büyük modeller (>1M vertex) daha uzun işleme süresi alır
- İşlem adımlarını tek tek uygulayıp kontrol edin
- Her adımı kaydetme şansınız var (geri alma özelliği)

## 🔍 Sorun Giderme

### "Model yüklenemedi" Hatası
- Dosya formatını kontrol edin (.stl veya .ply)
- Dosya boyutunun 50MB'ın altında olduğundan emin olun
- Dosyanın bozuk olmadığını kontrol edin

### "Analiz başarısız" Hatası
- Model dosyasının geçerli bir 3D mesh içerdiğinden emin olun
- Çok karmaşık modeller için vertex sayısını azaltmayı deneyin

### "İşlem başarısız" Hatası
- Parametreleri kontrol edin
- Daha önce başka bir işlem uygulamayı deneyin
- Model topolojisini düzeltin

### Görselleştirme Sorunları
- Tarayıcınızın WebGL desteğini kontrol edin
- Sayfayı yenileyin
- Başka bir tarayıcı deneyin

## ❓ SSS (Sık Sorulan Sorular)

**S: Hangi dosya formatları destekleniyor?**  
C: STL (binary ve ASCII) ve PLY formatları desteklenmektedir.

**S: Maksimum dosya boyutu nedir?**  
C: 50 MB

**S: İşlenen modeller ne kadar süre saklanır?**  
C: Tüm modelleriniz ve işlem geçmişiniz hesabınızda süresiz saklanır.

**S: Modeli 3D yazıcıda basabilir miyim?**  
C: Evet, export edilen STL dosyaları direkt olarak 3D yazıcılarda basılabilir.

**S: Birden fazla işlemi geri alabilir miyim?**  
C: Evet, her işlem adımı kaydedilir ve önceki versiyonlara dönebilirsiniz.

**S: Mobile cihazlarda çalışır mı?**  
C: Web arayüzü responsive tasarıma sahiptir, ancak en iyi deneyim için desktop önerilir.

## 📞 Destek

Sorunlarınız veya önerileriniz için:
- Email: alidoganbektas@gmail.com
- Dokümantasyon: [README.md](../README.md)
- Mimari: [ARCHITECTURE.md](ARCHITECTURE.md)
- API: [API_DOCS.md](API_DOCS.md)

---

**Son Güncelleme**: 2025-10-02

