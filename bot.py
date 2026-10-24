import os
import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎵 جست‌وجوی آهنگ با متن", callback_data="search")],
        [InlineKeyboardButton("🎤 تشخیص آهنگ از ویس یا کلیپ", callback_data="identify")],
    ]
    await update.message.reply_text(
        "🎧 به ACE MUSIC FINDER خوش اومدی!\n\n"
        "اسم آهنگ یا چند کلمه از متنش رو بفرست.\n"
        "برای تشخیص آهنگ، ویس یا کلیپ کوتاه هم ارسال کن.",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "search":
        await query.message.reply_text(
            "✍️ اسم آهنگ یا بخشی از متنش رو بفرست."
        )
    elif query.data == "identify":
        await query.message.reply_text(
            "🎤 یک ویس، فایل صوتی یا کلیپ کوتاه بفرست."
        )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    await update.message.reply_text(
        f"🔎 درخواست جست‌وجو: {text}\n\n"
        "⚠️ موتور جست‌وجوی آهنگ هنوز متصل نشده است. "
        "در مرحله بعد، منبع جست‌وجوی رایگان را اضافه می‌کنیم."
    )

async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎧 فایل دریافت شد!\n\n"
        "⚠️ سرویس تشخیص آهنگ هنوز متصل نشده است؛ "
        "در مرحله بعد این قابلیت را اضافه می‌کنیم."
    )

def main():
    if not TOKEN:
        raise RuntimeError("متغیر BOT_TOKEN تنظیم نشده است.")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(
        MessageHandler(
            filters.VOICE | filters.AUDIO | filters.VIDEO | filters.Document.ALL,
            handle_media,
        )
    )

    app.run_polling()

if __name__ == "__main__":
    main()
