# StokIzleme - Kurulum ve Çalıştırma Rehberi

## 🚀 Hızlı Başlangıç

Bu rehber, StokIzleme uygulamasını yerel geliştirme ortamınızda çalıştırmanız için gerekli adımları içerir.

## 📋 Gereksinimler

### Sistem Gereksinimleri
- **Windows 11** (mevcut sisteminiz)
- **Python 3.11+**
- **Flutter 3.16+**
- **Git**
- **Chrome Browser** (web scraping için)

### Geliştirme Araçları
- **Cursor IDE** (mevcut)
- **Android Studio** (Android emulator için)
- **Postman/Insomnia** (API test için)

## 🔧 Backend Kurulumu

### 1. Python Sanal Ortam Oluşturma
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows için
```

### 2. Bağımlılıkları Yükleme
```bash
pip install -r requirements.txt
```

### 3. Redis Kurulumu
Redis'i Windows'ta çalıştırmak için:

**Seçenek 1: Docker ile (Önerilen)**
```bash
docker run -d -p 6379:6379 redis:alpine
```

**Seçenek 2: Windows Subsystem for Linux (WSL)**
```bash
wsl
sudo apt update
sudo apt install redis-server
sudo service redis-server start
```

**Seçenek 3: Windows için Redis**
- [Redis for Windows](https://github.com/microsoftarchive/redis/releases) indirin
- Kurulumu tamamlayın
- Redis servisini başlatın

### 4. Veritabanı Başlatma
```bash
cd backend
python -c "from app.core.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

### 5. Backend'i Çalıştırma
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Celery Worker'ı Başlatma (Yeni Terminal)
```bash
cd backend
celery -A app.tasks.celery_app worker --loglevel=info
```

### 7. Celery Beat'i Başlatma (Yeni Terminal)
```bash
cd backend
celery -A app.tasks.celery_app beat --loglevel=info
```

## 📱 Frontend Kurulumu

### 1. Flutter Kurulumu
Flutter SDK'yı [flutter.dev](https://flutter.dev/docs/get-started/install/windows) adresinden indirin ve kurun.

### 2. Flutter Doctor
```bash
flutter doctor
```
Tüm gereksinimlerin karşılandığından emin olun.

### 3. Bağımlılıkları Yükleme
```bash
cd frontend
flutter pub get
```

### 4. Android Emulator Kurulumu
1. Android Studio'yu açın
2. AVD Manager'ı açın
3. Yeni bir Android Virtual Device oluşturun
4. Emulator'ü başlatın

### 5. Flutter Uygulamasını Çalıştırma
```bash
cd frontend
flutter run
```

## 🔥 Firebase Kurulumu (Bildirimler için)

### 1. Firebase Projesi Oluşturma
1. [Firebase Console](https://console.firebase.google.com/) gidin
2. Yeni proje oluşturun: "StokIzleme"
3. Android uygulaması ekleyin

### 2. Firebase Konfigürasyonu
1. `google-services.json` dosyasını indirin
2. `frontend/android/app/` klasörüne kopyalayın

### 3. Backend Firebase Ayarları
1. Firebase Console'da Project Settings > Service Accounts
2. "Generate new private key" tıklayın
3. JSON dosyasını `backend/firebase-credentials.json` olarak kaydedin
4. `backend/.env` dosyası oluşturun:

```env
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
FIREBASE_PROJECT_ID=your-project-id
```

## 🧪 Test Etme

### 1. Backend API Test
```bash
# Tarayıcıda açın
http://localhost:8000/docs
```

### 2. Örnek Wishlist Ekleme
```bash
curl -X POST "http://localhost:8000/api/v1/wishlists" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Zara Kış Koleksiyonu",
    "store_name": "zara",
    "url": "https://www.zara.com/tr/tr/wishlist",
    "auto_purchase": false
  }'
```

### 3. Flutter Uygulaması Test
1. Emulator'de uygulamayı açın
2. Wishlist ekleme ekranını test edin
3. Bildirimleri test edin

## 🐛 Sorun Giderme

### Backend Sorunları
1. **Redis bağlantı hatası**: Redis servisinin çalıştığından emin olun
2. **Port çakışması**: 8000 portunu kullanan başka uygulama var mı kontrol edin
3. **Python bağımlılık hatası**: `pip install -r requirements.txt` tekrar çalıştırın

### Frontend Sorunları
1. **Flutter doctor hataları**: Flutter kurulumunu kontrol edin
2. **Emulator sorunları**: Android Studio AVD Manager'ı kullanın
3. **API bağlantı hatası**: Backend'in çalıştığından emin olun

### Web Scraping Sorunları
1. **Chrome driver hatası**: `webdriver-manager` otomatik olarak indirecek
2. **Site erişim sorunu**: İnternet bağlantınızı kontrol edin
3. **Selector hatası**: Mağaza sitelerinin yapısı değişmiş olabilir

## 📁 Proje Yapısı

```
StokIzleme/
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Config, database
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   ├── tasks/          # Celery tasks
│   │   └── utils/          # Utilities
│   ├── requirements.txt
│   └── main.py
├── frontend/               # Flutter app
│   ├── lib/
│   │   ├── models/         # Data models
│   │   ├── services/       # API services
│   │   ├── providers/      # State management
│   │   ├── screens/        # UI screens
│   │   └── widgets/        # Reusable widgets
│   └── pubspec.yaml
└── docs/                   # Documentation
```

## 🚀 Production Deployment

### Backend (Heroku/DigitalOcean)
1. `Procfile` oluşturun
2. Environment variables ayarlayın
3. PostgreSQL veritabanı kullanın
4. Redis Cloud kullanın

### Frontend (Google Play Store)
1. Release build oluşturun
2. APK/AAB dosyası hazırlayın
3. Google Play Console'da yayınlayın

## 📞 Destek

Sorun yaşarsanız:
1. Bu README'yi tekrar okuyun
2. Flutter ve Python dokümantasyonlarını kontrol edin
3. GitHub Issues'da sorun bildirin

## 🎯 Sonraki Adımlar

1. **Web Scraping İyileştirmeleri**: Mağaza sitelerinin yapısına göre selector'ları güncelleyin
2. **Otomatik Satın Alma**: E-ticaret sitelerinin API'lerini entegre edin
3. **Fiyat Takibi**: Fiyat değişikliklerini izleyin
4. **Çoklu Mağaza**: Daha fazla mağaza ekleyin
5. **Kullanıcı Yönetimi**: Kullanıcı hesapları ve kimlik doğrulama ekleyin

---

**Not**: Bu uygulama kişisel kullanım için tasarlanmıştır. Ticari kullanım için ek geliştirmeler gerekebilir. 