# 🌍 Digital Twin – Istanbul IoT Simulation

Gerçek zamanlı IoT sensör verilerini simüle eden ve farklı çevresel senaryolar altında karşılaştırmalı analiz yapılmasını sağlayan bir **Digital Twin** uygulamasıdır.

---

## 🔧 Kullanım

### 1️⃣ Sistemi Başlat

- Sidebar’dan **▶ Sistemi Başlat** butonuna basın.
- İstanbul üzerinde rastgele konumlarda sensör node’ları oluşturulur.
- İlk veri snapshot’ı alınır.

---

### 2️⃣ Senaryo Seçimi

Sidebar üzerinden aşağıdaki senaryolardan biri seçilebilir:

- **Normal** → Referans (baz) veri
- **Sıcak Hava** → Sıcaklık artar, nem azalır
- **Nemli Ortam** → Nem artar
- **Düşük Batarya** → Batarya tüketimi hızlanır

---

### 3️⃣ Veri Güncelleme

- **🔄 Tek Güncelle** butonuna basarak tüm node’ları güncelleyebilirsiniz.
- Her güncellemede:
  - Sensör değerleri değişir
  - Delta (± fark) hesaplanır
  - Veriler CSV dosyasına kaydedilir

---

## 📊 Arayüz Davranışı

### 🟢 Normal Senaryo Seçiliyse

- Sağ panelde yalnızca Normal veriler gösterilir.
- Güncel değerler ve delta farkları görünür.
- Zaman serisi grafikleri gösterilir.

---

### 🟡 Normal Dışında Bir Senaryo Seçiliyse

- İki sütun halinde görüntülenir:
  - Sol → Normal değerler
  - Sağ → Seçili senaryo değerleri
- Her iki sütunda da delta (± fark) gösterilir.
- En altta Normal ile seçili senaryonun karşılaştırma grafiği bulunur.

---

### 📌 Gösterilecek Veri Seçimi

- **ALL** → Tüm metrikler (temperature, humidity, battery)
- **Temperature / Humidity / Battery** → Sadece seçilen metrik
- Tüm node görünümünde sütun grafik kullanılır.
- Tek node seçiliyse zaman serisi grafiği korunur.

---

## 🧩 Gereksinimler

- Python 3.9+
- Streamlit
- Folium
- streamlit-folium
- Pandas
- NumPy

Bağımlılıkları yüklemek için:

```bash
pip install streamlit folium streamlit-folium pandas numpy

---

## ▶️ Uygulamayı Çalıştırma

streamlit run app.py

Uygulama varsayılan olarak şu adreste açılır:

http://localhost:8501

### 📁 Proje Yapısı

├── app.py
├── simulation.py
├── weather.py
├── data/
│   └── sensor_log.csv
└── README.md

### 📌 Notlar

- Veriler data/sensor_log.csv dosyasına kaydedilir.
- Senaryo algoritmaları genişletilebilir.
- Gerçek hava API entegrasyonu eklenebilir.
- Demo ve akademik kullanım için uygundur.
- Dashboard yapısı geliştirilmeye açıktır.
