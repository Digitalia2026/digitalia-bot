import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("👩 Explorar creadoras", callback_data="explorar")],
        [InlineKeyboardButton("⭐ Mi saldo", callback_data="saldo")],
        [InlineKeyboardButton("🛒 Mis compras", callback_data="compras")],
        [InlineKeyboardButton("👤 Mi cuenta", callback_data="cuenta")],
        [InlineKeyboardButton("💰 Recargar", callback_data="recargar")],
        [InlineKeyboardButton("❓ Ayuda", callback_data="ayuda")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🌟 DIGITALIA\n\n"
        "👋 Bienvenido.\n"
        "Explora creadoras y descubre su contenido.",
        reply_markup=reply_markup
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
        "ayuda": "❓ Ayuda de Digitalia."
    }

    await query.edit_message_text(
        mensajes.get(query.data, "Opción no disponible.")
    )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        __import__("telegram.ext", fromlist=["CallbackQueryHandler"])
        .CallbackQueryHandler(botones)
    )

    app.run_polling()


if __name__ == "__main__":
    main()
