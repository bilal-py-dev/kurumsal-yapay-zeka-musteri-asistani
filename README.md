# 🤖 Kurumsal Yapay Zeka Müşteri Destek Asistanı (FastAPI + Gemini AI)

Şirketlerin veya e-ticaret sitelerinin kendi bilgi bankası belgelerini (`sirket_bilgileri.txt`) okuyarak müşteri sorularını 7/24 kesintisiz, nazik ve doğru şekilde yanıtlayan **Yapay Zeka Müşteri Destek API ve Canlı Sohbet Arayüzü**.

## 🚀 Özellikler
- **Şirket Verisine Dayalı Yanıtlar:** Yapay zeka yalnızca tanımlanan şirket kurallarını referans alır, bilgi dışı konularda uydurma cevap üretmez.
- **Konuşma Geçmişi Hafızası:** Müşterinin son mesajlarını hatırlayarak bağlamı koparmadan sohbeti sürdürür.
- **Otomatik Yedek Model Koruması:** Aktif Gemini modellerini otomatik listeler; bir modelde yoğunluk yaşanması durumunda kesintisiz olarak diğer modele geçiş yapar.
- **Hazır Web Sohbet Arayüzü (Chat UI) & Swagger UI:** Hem modern karanlık temalı sohbet penceresi hem de `/docs` üzerinden test edilebilir REST API sunar.

## 🛠️ Kurulum ve Çalıştırma
1. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
2. `main.py` içerisindeki `API_ANAHTARI` alanına kendi Google AI Studio anahtarınızı ekleyin.
3. Sunucuyu başlatın:
   ```bash
   uvicorn main:app --reload
   ```
4. Tarayıcınızda `http://127.0.0.1:8000` adresini açarak sohbet arayüzünü, `http://127.0.0` adresini açarak API dokümantasyonunu test edin.
