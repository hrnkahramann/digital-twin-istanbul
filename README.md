Digital Twin – Istanbul IoT Simulation

Bu proje, İstanbul konumları üzerinde sanal IoT sensör düğümleri oluşturarak çevresel verilerin (sıcaklık, nem ve batarya durumu) simülasyonunu yapan bir Digital Twin uygulamasıdır.
Uygulama, gerçek hava durumu verilerini kullanır ve bu verileri rastgelelik ve senaryo etkileri ile simüle eder.
Sonuçlar harita üzerinde görselleştirilir ve zaman içinde değişimleri grafiklerle izlenebilir.

📌 Projenin Amacı

İstanbul üzerinde sanal sensör düğümleri üretmek

Gerçek hava durumu verilerini kullanarak sıcaklık ve nem simülasyonu yapmak

Batarya tüketimi ve güneş enerjisi şarjını modellemek

Farklı senaryolar (sıcak hava, nemli ortam, düşük batarya) altında sistem davranışını gözlemlemek

Verileri harita ve grafikler ile görselleştirmek



⚙️ Kullanılan Teknolojiler

Python

Streamlit

Folium (harita)

OpenWeather API

Pandas

NumPy

📂 Proje Yapısı
digital-twin-istanbul/
│
├── app.py              → Streamlit arayüzü
├── simulation.py       → Sensör ve batarya simülasyonu
├── weather.py          → Hava durumu API bağlantısı
├── config.py           → Ortam değişkenleri ve sabitler
├── requirements.txt    → Gerekli kütüphaneler
├── data/
│   └── sensor_log.csv  → Üretilen verilerin kaydı
└── digitalTwin/
    ├── network.py
    ├── node.py
    └── simulator.py

🧪 Simüle Edilen Veriler

Her sensör düğümü için:

Sıcaklık (°C)

Nem (%)

Batarya seviyesi (%)

Batarya, güneş enerjisi üretimi ve tüketim modeline göre azalır veya artar.

🌦 Senaryolar

Uygulama içinde şu senaryolar bulunur:

Normal

Sıcak Hava → Sıcaklık artar, nem azalır, batarya daha hızlı düşer

Nemli Ortam → Nem artar, sıcaklık azalır

Düşük Batarya → Batarya seviyesi hızlı düşer

Senaryolar sensör verilerine yapay etki uygular.

🖥️ Uygulamayı Çalıştırma
1. Sanal ortam oluşturma
python -m venv venv

2. Sanal ortamı aktif etme

Windows:

venv\Scripts\activate


Linux / Mac:

source venv/bin/activate

3. Gerekli kütüphaneleri kurma
pip install -r requirements.txt

4. Ortam değişkenlerini ayarlama

.env dosyası oluştur:

OPENWEATHER_API_KEY=API_KEYİNİZ

5. Uygulamayı başlatma
streamlit run app.py


📊 Özellikler

Harita üzerinde sensör düğümleri

Heatmap ile yoğunluk gösterimi

Seçilen node için zaman serisi grafikler

Senaryo bazlı karşılaştırma

CSV olarak veri indirme

📝 Notlar

Bu proje eğitim ve simülasyon amaçlıdır.

Gerçek donanım verisi içermez, veriler matematiksel modelle üretilir.

OpenWeather API ücretsiz plan kullanıldığı için istek sınırı vardır.

Sensör konumları İstanbul sınırları içinde rastgele üretilir.

Batarya modeli ESP32 benzeri bir sistem varsayımıyla oluşturulmuştur.
