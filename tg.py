import json
from dotenv import load_dotenv
import os
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from main import *


load_dotenv()
TOKEN: Final = os.getenv("TOKEN")
DATA_FILE = "favori.json"  # Favori takımların saklanacağı dosya


# 📌 JSON dosyasından favorileri yükle
def load_favorites():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Dosya yoksa veya bozuksa boş bir liste döndür


# 📌 JSON dosyasına favorileri kaydet
def save_favorites(favorites):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(favorites, file, ensure_ascii=False, indent=4)


# Kullanıcının favori takımlarını tutan liste
favorite_teams = load_favorites()


def load_favorites():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("favorite_teams", [])  # "favorite_teams" anahtarını kontrol et
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Dosya yoksa veya bozuksa boş bir liste döndür


# 📌 JSON dosyasına favorileri kaydet
def save_favorites(favorites):
    data = {"favorite_teams": favorites}  # "favorite_teams" anahtarını kullanarak listeyi sakla
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# Kullanıcının favori takımlarını tutan liste
favorite_teams = load_favorites()


# 📌 /start - Başlangıç mesajı
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚽ Merhaba! Ben senin maç bildirim botunum.\n"
                                    "Favori takımlarını kaydedip maç günlerini takip edebilirim.\n"
                                    "📌 Komutlar için /help yazabilirsin!")


# 📌 /help - Komutları göster
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📌 Kullanılabilir Komutlar:\n"
                                    "/ekle <takım_adı> - Favori takıma ekle\n"
                                    "/sil <takım_adı> - Favori takımdan çıkar\n"
                                    "/liste - Favori takımları göster\n"
                                    "/maclar - Bugünkü maçlarını göster")


# 📌 /ekle <takım_adı> - Favori takıma ekleme
async def add_favorite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("❗ Lütfen bir takım adı girin: /ekle Galatasaray")
        return

    team = " ".join(context.args)  # Takım ismini al
    if team not in favorite_teams:
        favorite_teams.append(team)
        save_favorites(favorite_teams)  # JSON dosyasına kaydet
        await update.message.reply_text(f"✅ {team} favori takımlarına eklendi!")
    else:
        await update.message.reply_text(f"⚠️ {team} zaten favori takımlarında var.")


# 📌 /sil <takım_adı> - Favori takımdan silme
async def remove_favorite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("❗ Lütfen bir takım adı girin: /sil Fenerbahçe")
        return

    team = " ".join(context.args)
    if team in favorite_teams:
        favorite_teams.remove(team)
        save_favorites(favorite_teams)  # JSON'a kaydet
        await update.message.reply_text(f"❌ {team} favorilerinden çıkarıldı.")
    else:
        await update.message.reply_text(f"⚠️ {team} favori takımlarında bulunamadı.")


# 📌 /liste - Favori takımları listeleme
async def list_favorites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if favorite_teams:
        await update.message.reply_text(f"📌 Favori Takımların:\n- " + "\n- ".join(favorite_teams))
    else:
        await update.message.reply_text("⚠️ Henüz favori takım eklenmemiş.")



async def find_match(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teams = load_favorites()
    
    # Selenium fonksiyonunu çağırarak maçları al
    found_matches = find_matches_for_teams(teams)

    if found_matches:
        await update.message.reply_text(f"Bugün oynanacak maçlar:\n" + "\n".join(found_matches))
    else:
        await update.message.reply_text("Belirtilen takım(lar) için bugün maç bulunamadı.")
if __name__ == "__main__":
    print("Starting bot..")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("ekle", add_favorite))
    app.add_handler(CommandHandler("sil", remove_favorite))
    app.add_handler(CommandHandler("liste", list_favorites))
    app.add_handler(CommandHandler("maclar", find_match))
    

    print("Polling..")
    app.run_polling(poll_interval=3)
