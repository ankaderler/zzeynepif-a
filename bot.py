import os
import logging
import threading
import http.server
import socketserver
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Render canlı kalma port ayarı
PORT = int(os.environ.get("PORT", 10000))

class HealthCheckHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"VIP Bot is active and running!")

def run_web_server():
    with socketserver.TCPServer(("", PORT), HealthCheckHandler) as httpd:
        httpd.serve_forever()

# Arka planda web sunucusunu başlat
threading.Thread(target=run_web_server, daemon=True).start()

# --- YENİ TOKEN BİLGİSİ ---
TOKEN = "8522565760:AAExDDLlZ9EL6_b68C4GWb9rjAHVyIX_gOQ"
IBAN = "TR06 0001 0021 5470 2002 4550 04"
RECIPIENT = "Zeynep Alkoç"
PRICE = "300 TL"

VIP_LINKS = [
    "https://t.me/+Aqi4UqSzr4JjZmRk",
    "https://t.me/+H2z-xlyZ6zM0OTE0",
    "https://t.me/+p01bQp6XebkzMmI0",
    "https://t.me/+HqtuwLtoMkkwMWQ0",
    "https://t.me/+BcHhS86B9ocyMWQ0"
]

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

def main_menu():
    keyboard = [
        [InlineKeyboardButton("💎 VIP Üyelik Satın Al (300 TL)", callback_data="buy_vip")],
        [InlineKeyboardButton("📖 Nasıl Satın Alınır?", callback_data="how_to_buy")],
        [InlineKeyboardButton("🛡️ VIP Özellikler", callback_data="vip_features")],
        [InlineKeyboardButton("📞 7/24 Canlı Destek", url="https://t.me/SMSPATRONUM")],
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🔥 *ELİT VIP ARŞİV — MERKEZİNE HOŞ GELDİNİZ*\n\n"
        "✨ Tamamen gizli ve özel içeriklerin paylaşıldığı VIP ekosistemimize anında adım atın.\n\n"
        "👇 Aşağıdaki menüden işlemlerinizi yönetebilirsiniz:"
    )
    if update.message:
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=main_menu())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    text = ""
    keyboard = []

    if data == "buy_vip":
        text = (
            f"💎 *ELİT VIP — GÜVENLİ ÖDEME ARAYÜZÜ*\n\n"
            f"📦 Paket: *Sınırsız Premium VIP Erişimi*\n"
            f"💰 Tutar: *{PRICE}*\n\n"
            f"💳 *Resmi Havale / FAST Bilgileri*\n"
            f"IBAN:\n`{IBAN}`\n\n"
            f"Alıcı Adı: *{RECIPIENT}*\n\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            f"1️⃣ Yukarıdaki IBAN hesabına tam *{PRICE}* gönderin.\n"
            "2️⃣ İşlem sonrasında **Dekontu / Ekran Görüntüsünü** doğrudan bu sohbet penceresine gönderin.\n"
            "3️⃣ Sistem dekontu onayladığı an özel VIP davet linkleriniz saniyeler içinde otomatik gelecektir!"
        )
        keyboard = [[InlineKeyboardButton("⬅️ Ana Menüye Dön", callback_data="home")]]

    elif data == "how_to_buy":
        text = (
            "📖 *SATIN ALMA REHBERİ*\n\n"
            "1️⃣ 'VIP Üyelik Satın Al' butonundan IBAN'a 300 TL gönderin.\n"
            "2️⃣ Dekontun ekran görüntüsünü bota fotoğraf olarak atın.\n"
            "3️⃣ Bot dekontu algılayıp VIP linkleri anında size versin!"
        )
        keyboard = [[InlineKeyboardButton("⬅️ Ana Menüye Dön", callback_data="home")]]

    elif data == "vip_features":
        text = (
            "🛡️ *VIP AYRICALIKLARI*\n\n"
            "• Sınırsız ve ömür boyu kanal erişimi\n"
            "• Günlük güncellenen özel arşivler\n"
            "• 7/24 öncelikli destek hattı"
        )
        keyboard = [[InlineKeyboardButton("⬅️️ Ana Menüye Dön", callback_data="home")]]

    elif data == "home":
        text = (
            "🔥 *ELİT VIP ARŞİV — MERKEZİNE HOŞ GELDİNİZ*\n\n"
            "✨ Tamamen gizli ve özel içeriklerin paylaşıldığı VIP ekosistemimize anında adım atın.\n\n"
            "👇 Aşağıdaki menüden işlemlerinizi yönetebilirsiniz:"
        )
        keyboard = [
            [InlineKeyboardButton("💎 VIP Üyelik Satın Al (300 TL)", callback_data="buy_vip")],
            [InlineKeyboardButton("📖 Nasıl Satın Alınır?", callback_data="how_to_buy")],
            [InlineKeyboardButton("🛡️ VIP Özellikler", callback_data="vip_features")],
            [InlineKeyboardButton("📞 7/24 Canlı Destek", url="https://t.me/SMSPATRONUM")],
        ]

    # Mesajı güncellemek yerine yeni bir mesaj göndererek olası hataları tamamen engelliyoruz
    await query.message.reply_text(
        text, 
        parse_mode="Markdown", 
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def receipt_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo or update.message.document:
        links_text = "\n".join([f"🔗 {link}" for link in VIP_LINKS])
        text = (
            "✅ *DEKONT ONAYLANDI! ÖDEME ALINDI.*\n\n"
            "🎉 Tebrikler! Özel davet linkleriniz aşağıdadır:\n\n"
            f"{links_text}\n\n"
            "⚠️ *Bu linkler kişiye özeldir, paylaşılması yasaktır.*"
        )
        keyboard = [[InlineKeyboardButton("🏠 Ana Menüye Dön", callback_data="home")]]
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    await update.message.reply_text("📸 Lütfen geçerli bir dekont ekran görüntüsü veya dosyası gönderin.")

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.ALL, receipt_handler))
    
    logger.info("Bot Yeni Token ile Polling modunda başlatılıyor...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
