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

    if query.data == "explorar":
        botones_creadoras = [
            [InlineKeyboardButton(
                "👩 Ana — Desde 300 puntos",
                callback_data="ana"
            )],
            [InlineKeyboardButton(
                "⬅️ Volver",
                callback_data="inicio"
            )],
        ]

        await query.edit_message_text(
            "🌟 CREADORAS DISPONIBLES\n\n"
            "👩 Ana\n"
            "✨ Contenido exclusivo\n"
            "💰 Desde 300 puntos",
            reply_markup=InlineKeyboardMarkup(botones_creadoras),
        )

    elif query.data == "ana":
        botones_ana = [
            [InlineKeyboardButton(
                "📸 Foto — 300 puntos",
                callback_data="foto"
            )],
            [InlineKeyboardButton(
                "🎥 Video — 700 puntos",
                callback_data="video"
            )],
            [InlineKeyboardButton(
                "📞 Tiempo privado — 20 puntos/min",
                callback_data="llamada"
            )],
            [InlineKeyboardButton(
                "⬅️ Volver",
                callback_data="explorar"
            )],
        ]

        await query.edit_message_text(
            "👩 ANA\n\n"
            "✨ Contenido exclusivo\n\n"
            "📸 Foto — 300 puntos\n"
            "🎥 Video — 700 puntos\n"
            "📞 Tiempo privado — 20 puntos/min\n\n"
            "Selecciona una opción:",
            reply_markup=InlineKeyboardMarkup(botones_ana),
        )

    elif query.data == "foto":
        await query.edit_message_text(
            "📸 FOTO DE ANA\n\n"
            "💰 Precio: 300 puntos\n\n"
            "🔓 Próximamente podrás desbloquearla."
        )

    elif query.data == "video":
        await query.edit_message_text(
            "🎥 VIDEO DE ANA\n\n"
            "💰 Precio: 700 puntos\n\n"
            "🔓 Próximamente podrás desbloquearlo."
        )

    elif query.data == "llamada":
        await query.edit_message_text(
            "📞 TIEMPO PRIVADO\n\n"
            "💰 Precio: 20 puntos por minuto\n\n"
            "🔓 Próximamente podrás solicitarlo."
        )

    elif query.data == "inicio":
        await start(update, context)

    elif query.data == "saldo":
        await query.edit_message_text(
            "⭐ Tu saldo actual es de 0 puntos."
        )

    elif query.data == "compras":
        await query.edit_message_text(
            "🛒 Aquí aparecerán tus compras."
        )

    elif query.data == "cuenta":
        await query.edit_message_text(
            "👤 Aquí aparecerán los datos de tu cuenta."
        )

    elif query.data == "recargar":
        await query.edit_message_text(
            "💰 La recarga estará disponible próximamente."
        )

    elif query.data == "ayuda":
        await query.edit_message_text(
            "❓ AYUDA\n\n"
            "Si necesitas ayuda, podrás contactar con Digitalia."
        )


def main():
    Thread(target=iniciar_web, daemon=True).start()

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(botones))

    print("Digitalia: bot iniciado correctamente.")

    application.run_polling()


if __name__ == "__main__":
    main()
