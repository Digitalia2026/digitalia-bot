import os
from threading import Thread

from flask import Flask
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

web = Flask(__name__)


@web.route("/")
def home():
    return "🖤🔥 Velvet Musa funcionando 😈"


def run_web():
    port = int(os.environ.get("PORT", 10000))
    web.run(host="0.0.0.0", port=port)


ES = {
    "home": "🏠 Inicio",
    "user": "👤 Soy Usuario 😏",
    "model": "🔥 Soy Modelo 💋",
    "agency": "🏢 Soy Agencia 😈",
    "language": "🌎 Idioma",
    "welcome": (
        "🖤🔥 VELVET MUSA 🔥🖤\n\n"
        "🌙 Hay noches que empiezan con un simple «hola»… 😈\n\n"
        "💋 Conoce a nuestras Musas\n"
        "✨ Elige la que despierte tu curiosidad\n"
        "💬 Habla con ella\n"
        "📸 Descubre su contenido privado\n"
        "📞 Comparte un momento a solas 🔥\n\n"
        "😈 Quizás encuentres exactamente lo que estabas buscando…\n\n"
        "👇 Elige una opción:"
    ),
    "user_title": "👤💎 MODO USUARIO 💎👤",
    "user_menu": (
        "🔎 Explorar Musas\n"
        "⭐ Mi saldo\n"
        "💰 Recargar saldo\n"
        "🛍️ Mis compras\n"
        "📞 Mis llamadas\n"
        "👤 Mi perfil"
    ),
    "model_title": "🔥💋 MODO MODELO 💋🔥",
    "model_menu": (
        "👤 Mi perfil\n"
        "📸 Mi contenido\n"
        "➕ Publicar contenido\n"
        "💰 Mis ganancias\n"
        "📊 Mis ventas\n"
        "📞 Mis llamadas\n"
        "🏢 Mi agencia\n"
        "💸 Solicitar retiro"
    ),
    "agency_title": "🏢🔥 MODO AGENCIA 🔥🏢",
    "agency_menu": (
        "👩‍👩‍👧 Mis Musas\n"
        "➕ Reclutar Musa\n"
        "🔑 Mis códigos\n"
        "📊 Ventas del equipo\n"
        "💰 Mis comisiones\n"
        "💸 Solicitar retiro\n"
        "📝 Mi agencia\n"
        "🏗️ Crear agencia"
    ),
    "language_title": (
        "🌎 IDIOMA\n\n"
        "🇪🇸 Español activado\n"
        "🇺🇸 English available"
    ),
    "coming": (
        "🚀🔥 PRÓXIMAMENTE 🔥\n\n"
        "Estamos preparando esta función para Velvet Musa. 🖤😈"
    ),
    "language_changed": "🇪🇸 Español activado 🖤🔥"
}


EN = {
    "home": "🏠 Home",
    "user": "👤 I'm a User 😏",
    "model": "🔥 I'm a Model 💋",
    "agency": "🏢 I'm an Agency 😈",
    "language": "🌎 Language",
    "welcome": (
        "🖤🔥 VELVET MUSA 🔥🖤\n\n"
        "🌙 Some nights start with a simple «hello»… 😈\n\n"
        "💋 Meet our Muses\n"
        "✨ Choose the one who catches your eye\n"
        "💬 Talk to her\n"
        "📸 Discover her private content\n"
        "📞 Spend some private time together 🔥\n\n"
        "😈 You might find exactly what you've been looking for…\n\n"
        "👇 Choose an option:"
    ),
    "user_title": "👤💎 USER MODE 💎👤",
    "user_menu": (
        "🔎 Explore Muses\n"
        "⭐ My balance\n"
        "💰 Add balance\n"
        "🛍️ My purchases\n"
        "📞 My calls\n"
        "👤 My profile"
    ),
    "model_title": "🔥💋 MODEL MODE 💋🔥",
    "model_menu": (
        "👤 My profile\n"
        "📸 My content\n"
        "➕ Publish content\n"
        "💰 My earnings\n"
        "📊 My sales\n"
        "📞 My calls\n"
        "🏢 My agency\n"
        "💸 Request withdrawal"
    ),
    "agency_title": "🏢🔥 AGENCY MODE 🔥🏢",
    "agency_menu": (
        "👩‍👩‍👧 My Muses\n"
        "➕ Recruit a Muse\n"
        "🔑 My codes\n"
        "📊 Team sales\n"
        "💰 My commissions\n"
        "💸 Request withdrawal\n"
        "📝 My agency\n"
        "🏗️ Create agency"
    ),
    "language_title": (
        "🌎 LANGUAGE\n\n"
        "🇺🇸 English activated\n"
        "🇪🇸 Español disponible"
    ),
    "coming": (
        "🚀🔥 COMING SOON 🔥\n\n"
        "We're preparing this feature for Velvet Musa. 🖤😈"
    ),
    "language_changed": "🇺🇸 English activated 🖤🔥"
}


def get_texts(context):
    if context.user_data.get("language") == "en":
        return EN
    return ES


def bottom_menu(t):
    return ReplyKeyboardMarkup(
        [
            [t["home"], t["user"]],
            [t["model"], t["agency"]],
            [t["language"]]
        ],
        resize_keyboard=True,
        is_persistent=True
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "language" not in context.user_data:
        code = update.effective_user.language_code or "es"

        if code.lower().startswith("en"):
            context.user_data["language"] = "en"
        else:
            context.user_data["language"] = "es"

    t = get_texts(context)

    await update.message.reply_text(
        t["welcome"],
        reply_markup=bottom_menu(t)
    )


async def messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = get_texts(context)
    text = update.message.text

    if text == t["home"]:
        await start(update, context)
        return

    if text == t["user"]:
        await update.message.reply_text(
            t["user_title"] + "\n\n" + t["user_menu"],
            reply_markup=bottom_menu(t)
        )
        return

    if text == t["model"]:
        await update.message.reply_text(
            t["model_title"] + "\n\n" + t["model_menu"],
            reply_markup=bottom_menu(t)
        )
        return

    if text == t["agency"]:
        await update.message.reply_text(
            t["agency_title"] + "\n\n" + t["agency_menu"],
            reply_markup=bottom_menu(t)
        )
        return

    if text == t["language"]:
        current = context.user_data.get("language", "es")

        if current == "es":
            context.user_data["language"] = "en"
        else:
            context.user_data["language"] = "es"

        t = get_texts(context)

        await update.message.reply_text(
            t["language_changed"],
            reply_markup=bottom_menu(t)
        )
        return

    await update.message.reply_text(
        t["coming"],
        reply_markup=bottom_menu(t)
    )


def main():
    Thread(
        target=run_web,
        daemon=True
    ).start()

    application = Application.builder().token(TOKEN).build()

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            messages
        )
    )

    print("🌟 Velvet Musa: bot iniciado correctamente 🔥")

    application.run_polling()


if __name__ == "__main__":
    main()
