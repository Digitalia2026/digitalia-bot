import os
from threading import Thread

from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")

app_web = Flask(__name__)


@app_web.route("/")
def inicio():
    return "Digitalia está funcionando."


def iniciar_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host="0.0.0.0", port=port)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    botones = [
        [InlineKeyboardButton("👩 Explorar creadoras", callback_data="explorar")],
        [InlineKeyboardButton("⭐ Mi saldo", callback_data="saldo")],
        [InlineKeyboardButton("🛒 Mis compras", callback_data="compras")],
        [InlineKeyboardButton("👤 Mi cuenta", callback_data="cuenta")],
        [InlineKeyboardButton("💰 Recargar", callback_data="recargar")],
        [InlineKeyboardButton("❓ Ayuda", callback_data="ayuda")],
    ]

    await update.message.reply_text(
        "🌟 DIGITALIA\n\n"
        "👋 Bienvenido.\n"
        "Explora creadoras y descubre su contenido.",
        reply_markup=InlineKeyboardMarkup(botones),
    )


async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    mensajes = {
        "explorar": "👩 Aquí aparecerán las creadoras disponibles.",
        "saldo": "⭐ Tu saldo: 0 puntos.",
        "compras": "🛒 Aquí aparecerán tus compras.",
        "cuenta": "👤 Aquí aparecerán los datos de tu cuenta.",
        "recargar": "💰 Próximamente podrás recargar tu saldo.",
        "ayuda": "❓ Ayuda de Digitalia.",
    }

    await query.edit_message_text(
        mensajes.get(query.data, "Opción no disponible.")
    )


def main():
    # Iniciar la página web en segundo plano
    Thread(target=iniciar_web, daemon=True).start()

    # Iniciar el bot de Telegram
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(botones))

    print("Digitalia: bot iniciado correctamente.")

    application.run_polling()


if __name__ == "__main__":
    main()
