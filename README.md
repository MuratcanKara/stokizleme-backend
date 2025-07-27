# StokIzleme - Wishlist Stok Takip Uygulaması

## 📱 Proje Açıklaması
Bu uygulama, Zara, Bershka, Pull&Bear gibi mağazaların wishlist'lerindeki ürünlerin stok durumunu takip eder ve stok geldiğinde anında bildirim gönderir.

## 🏗️ Mimari
- **Backend**: Python FastAPI + Celery
- **Frontend**: Flutter (Android)
- **Veritabanı**: SQLite (dev) / PostgreSQL (prod)
- **Bildirimler**: Firebase Cloud Messaging

## 🚀 Kurulum

### Backend Kurulumu
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Kurulumu
```bash
cd frontend
flutter pub get
```

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

## 🔧 Çalıştırma
1. Backend: `cd backend && uvicorn main:app --reload`
2. Frontend: `cd frontend && flutter run`

## 📋 Özellikler
- [x] Wishlist ekleme/düzenleme
- [x] Otomatik stok kontrolü
- [x] Push bildirimleri
- [x] Otomatik satın alma (gelecek)
- [ ] Çoklu mağaza desteği
- [ ] Fiyat takibi 