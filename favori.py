import json

# JSON dosyasından takımları yükle
def favori_takimlari_yukle():
    try:
        with open("favori.json", "r", encoding="utf-8") as file:
            return json.load(file).get("favori", [])
    except FileNotFoundError:
        return []

# JSON dosyasına takımları kaydet
def favori_takimlari_kaydet(takimlar):
    with open("favori.json", "w", encoding="utf-8") as file:
        json.dump({"favori": takimlar}, file, indent=4, ensure_ascii=False)

# Takım ekleme fonksiyonu
def favori_ekle(takim):
    takimlar = favori_takimlari_yukle()
    
    if takim not in takimlar:
        takimlar.append(takim)
        favori_takimlari_kaydet(takimlar)
        print(f"✅ {takim} favorilere eklendi!")
    else:
        print(f"⚠️ {takim} zaten favorilerinde var!")

# Favori takımları listeleme fonksiyonu
def favorilerim():
    return favori_takimlari_yukle()

# Takım silme fonksiyonu
def favori_sil(takim):
    takimlar = favori_takimlari_yukle()
    
    if takim in takimlar:
        takimlar.remove(takim)
        favori_takimlari_kaydet(takimlar)
        print(f"🗑️ {takim} favorilerinden silindi!")
    else:
        print(f"❌ {takim} zaten favorilerinde yok!")
