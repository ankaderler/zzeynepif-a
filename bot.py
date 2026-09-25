import logging
import os
from threading import Thread
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Logging ayarları
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Yeni Token
TOKEN = "8659358008:AAHFKg3notOSzpqFfZv7ibkocs4e3ixYMOY"

# Ödeme Bilgileri
IBAN = "TR06 0001 0021 5470 2002 4550 04"
ALICI_ADI = "Zeynep Alkoç"
TUTAR = "400 TL"

# Teslim edilecek VIP Linkler
VIP_LINKLER = (
    "🎉 **Ödemeniz Onaylandı!** 🎉\n\n"
    "İşte Zeynep VIP Arşivi ve Özel Linkleriniz:\n"
    "🔗 [Arşivi Görüntüle ve İndir](https://t.me/+orneklinkiniz)\n\n"
    "🎁 **Hediye:** 20 Dakika Ücretsiz Şov Hakkınız tanımlanmıştır!"
)

# --- RENDER WEB SERVİSİ İÇİN SAHTE SUNUCU (Port Hatasını Önler) ---
app = Flask("")


@app.route("/")
def home():
  return "Bot aktif ve çalışıyor!"


def run_web():
  port = int(os.environ.get("PORT", 10000))
  app.run(host="0.0.0.0", port=port)


def keep_alive():
  t = Thread(target=run_web)
  t.start()
# -------------------------------------------------------------


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_name = update.effective_user.first_name

  text = (
      f"⭐ Merhaba **{user_name}**, Zeynep'in Arşivi için ödeme bilgileri"
      f" aşağıdadır:\n\n"
      f"👤 Alıcı: **{ALICI_ADI}**\n"
      f"💳 IBAN: `{IBAN}`\n"
      f"💰 Tutar: **{TUTAR}**\n\n"
      "🎁 *Not:* Arşivi alan herkese **20 dk show ücretsizdir!**\n\n"
      "Ödemeyi yaptıktan sonra dekontunuzun ekran görüntüsünü bu sohbete"
      " gönderin."
  )

  await update.message.reply_text(text, parse_mode="Markdown")


async def foto_veya_belge_geldi(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
  user = update.effective_user

  keyboard = [[
      InlineKeyboardButton(
          f"✅ Onayla و Link Ver ({user.id})",
          callback_data=f"onayla_{user.id}",
      )
  ]]
  reply_markup = InlineKeyboardMarkup(keyboard)

  await update.message.reply_text(
      "⏳ Dekontunuz alındı! Yönetici kontrol ediyor, onaylandığı an linkler"
      " gelecektir."
  )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()

  data = query.data
  if data.startswith("onayla_"):
    hedef_user_id = int(data.split("_")[1])

    try:
      await context.bot.send_message(
          chat_id=hedef_user_id, text=VIP_LINKLER, parse_mode="Markdown"
      )
      await query.edit_message_text(
          text="✅ Ödeme onaylandı ve linkler müşteriye başarıyla iletildi!"
      )
    except Exception as e:
      await query.edit_message_text(
          text=f"❌ Gönderim başarısız oldu: {e}"
      )


def main():
  # Web sunucusunu arka planda başlat (Render port sorununu çözer)
  keep_alive()

  application = ApplicationBuilder().token(TOKEN).build()

  application.add_handler(CommandHandler("start", start))
  application.add_handler(
      MessageHandler(filters.PHOTO | filters.Document.ALL, foto_veya_belge_geldi)
  )
  application.add_handler(CallbackQueryHandler(button_handler))

  print("Bot başarıyla başlatıldı ve çalışıyor...")
  application.run_polling()


if __name__ == "__main__":
  main()
