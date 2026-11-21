from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Dict
from google import genai
import os

# Google AI Studio'dan aldığın anahtarı buraya yapıştır
import os

# Anahtarı kodun içine doğrudan yazmak yerine ortam değişkeninden veya kullanıcıdan alır
API_ANAHTARI = os.getenv("GEMINI_API_KEY", "BURAYA_GEMINI_API_ANAHTARINI_YAZIN")


client = genai.Client(api_key=API_ANAHTARI)
app = FastAPI(title="Kurumsal Yapay Zeka Müşteri Destek Sistemi")

class SoruIstegi(BaseModel):
    musteri_adi: str = "Müşteri"
    soru: str
    gecmis: List[Dict[str, str]] = []

def bilgi_bankasi_oku():
    if os.path.exists("sirket_bilgileri.txt"):
        with open("sirket_bilgileri.txt", "r", encoding="utf-8") as f:
            return f.read()
    return ""

@app.get("/", response_class=HTMLResponse)
def web_arayuzu():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/soru-sor")
def musteri_sorusu_yanitla(istek: SoruIstegi):
    bilgiler = bilgi_bankasi_oku()
    if not bilgiler:
        raise HTTPException(status_code=500, detail="Şirket bilgi dosyası bulunamadı.")

    gecmis_metni = ""
    for adim in istek.gecmis[-5:]:
        gecmis_metni += f"Müşteri: {adim.get('kullanici', '')}\nAsistan: {adim.get('asistan', '')}\n"

    prompt = f"""
    Sen NovaTeknoloji firmasının nazik ve profesyonel müşteri destek asistanısın.
    Yalnızca aşağıdaki şirket bilgilerine dayanarak kısa, net ve Türkçe yanıt ver.
    Cevap şirket bilgilerinde yoksa uydurma ve 'Bu konuda net bilgim bulunmuyor, 0850 000 00 00 WhatsApp hattımızdan destek alabilirsiniz.' de.

    ŞİRKET BİLGİLERİ:
    {bilgiler}

    ÖNCEKİ KONUŞMA GEÇMİŞİ:
    {gecmis_metni}

    YENİ MÜŞTERİ SORUSU:
    {istek.soru}
    """

    aktif_modeller = [
        m.name.replace("models/", "")
        for m in client.models.list()
        if "gemini" in m.name and ("flash" in m.name or "pro" in m.name)
    ]

    son_hata = ""
    for model_adi in aktif_modeller:
        try:
            cevap = client.models.generate_content(
                model=model_adi,
                contents=prompt,
            )
            return {
                "musteri": istek.musteri_adi,
                "soru": istek.soru,
                "kullanilan_model": model_adi,
                "yapay_zeka_yaniti": cevap.text.strip()
            }
        except Exception as e:
            son_hata = str(e)
            continue

    raise HTTPException(status_code=503, detail=f"Tüm modeller şu an yoğun: {son_hata}")

