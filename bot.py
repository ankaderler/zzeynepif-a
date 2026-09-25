import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

# Logging ayarları
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Size iletilen Bot Token
TOKEN = "8659358008:AAEo39bjF47ZheASqwLPpmz_AjvNyKHfHC8"

# Ödeme Bilgileri
IBAN = "TRXX XXXX XXXX XXXX XXXX XXXX XX"  # Buraya Zeynep Alkoç'a ait IBAN numaranızı tam olarak yazabilirsiniz
ALICI_ADI = "Zeynep Alkoç"
TUTAR = "400 TL"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  # Gold VIP Tasarımlı Karşılama Mesajı
  user_name = update.effective_user.first_name

  text = (
      "⭐ *ZEYNEP VIP ARCHIVE - GOLD EDITION* ⭐\n\n"
      f"Hoş geldin, **{user_name}**!\n\n"
      "👑 Özel arşive erişim sağlamak ve **Gold VIP** ayrıcalıklarından "
      "faydalanmak üzeresin.\n\n"
      "💎 *İçerik Detayları:*\n"
      "• Sınırsız ve Güncel Arşiv Erişimi\n"
      "• Gizli Özel Linkler\n"
      "• VIP Üyelere Özel Güncellemeler\n\n"
      "💳 *Ödeme Bilgileri:*\n"
      f"• Alıcı: **{ALICI_ADI}**\n"
      f"• Tutar: **{TUTAR}**\n"
      f"• IBAN: `{IBAN}`\n\n"
      "⚠️ *Önemli Not:* Ödemeyi gerçekleştirdikten sonra altta bulunan "
      '"💸 Ödemeyi Yaptım / Bildir" butonuna basarak dekontunuzu '
      "yöneticiye iletebilirsiniz."
  )

  keyboard = [[
      InlineKeyboardButton(
          "💸 Ödemeyi Yaptım / Bildir", callback_data="odeme_bildir"
      )
  ]]
  reply_markup = InlineKeyboardMarkup(keyboard)

  await update.message.reply_text(
      text, reply_markup=reply_markup, parse_mode="Markdown"
  )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()

  if query.data == "odeme_bildir":
    await query.message.reply_text(
        "✅ Ödeme bildirimin alındı!\n\n"
        "Lütfen ödemeye ait ekran görüntüsünü/dekontu bu sohbete gönder. "
        "Yönetici kontrol ettikten sonra **Gold VIP** özel linklerin "
        "tarafına iletilecektir. 🚀"
    )


def main():
  # Uygulama başlatıcı
  application = ApplicationBuilder().token(TOKEN).build()

  # Komutlar ve Buton Dinleyicileri
  application.add_handler(CommandHandler("start", start))
  application.add_handler(CallbackQueryHandler(button_handler))

  print("Bot başarıyla başlatıldı ve çalışıyor...")
  application.run_polling()


if __name__ == "__main__":
  main()
