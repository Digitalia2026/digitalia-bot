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
    "language": "🌎 Idioma"
}

EN = {
    "home": "🏠 Home",
    "user": "👤 I'm a User 😏",
    "model": "🔥 I'm a Model 💋",
    "agency": "🏢 I'm an Agency 😈",
    "language": "🌎 Language"
}

def get_texts(context):
    if context.user_data.get("language") == "en":
        return EN
    return ES

def menu(t):
    return ReplyKeyboardMarkup(
        [
            [t["home"], t["user"]],
            [t["model"], t["agency"]],
            [t["language"]]
        ],
        resize_keyboard=True
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if "language" not in context.user_data:
        code = update.effective_user.language_code or "es"

        if code.lower().startswith("en"):
            context.user_data["language"] = "en"
        else:
            context.user_data["language"] = "es"

    t = get_texts(context)

    if context.user_data["language"] == "en":
        mensaje = """🖤🔥 VELVET MUSA 🔥🖤

🌙 Some nights start with a simple “hello”… 😈

💋 Meet our Muses
✨ Choose the one who catches your eye
💬 Talk to her
📸 Discover her private content
📞 Spend some private time together 🔥

😈 You might find exactly what you've been looking for…

👇 What are you looking for?"""
    else:
        mensaje = """🖤🔥 VELVET MUSA 🔥🖤

🌙 Hay noches que empiezan con un simple “hola”… 😈

💋 Conoce a nuestras Musas
✨ Elige la que despierte tu curiosidad
💬 Habla con ella
📸 Descubre su contenido privado
📞 Comparte un momento a solas 🔥

😈 Quizás encuentres exactamente lo que estabas buscando…

👇 ¿Qué estás buscando?"""

    await update.message.reply_text(
        mensaje,
        reply_markup=menu(t)
    )

async def messages(update: Update, context: ContextTypes.DEFAULT_TYPE):

    t = get_texts(context)
    text = update.message.text

    if text == t["language"]:

        context.user_data["language"] = (
            "en"
            if context.user_data.get("language") != "en"
            else "es"
        )

        t = get_texts(context)

        await update.message.reply_text(
            "🌎 Language / Idioma\n\n"
            + (
                "🇺🇸 English activated!"
                if context.user_data["language"] == "en"
                else "🇪🇸 ¡Español activado!"
            ),
            reply_markup=menu(t)
        )

    elif text == t["home"]:

        await start(update, context)

    elif text == t["user"]:

        await update.message.reply_text(
            "👤💎 USER MODE 💎\n\n"
            "🔎 Explore Muses\n"
            "⭐ Check balance\n"
            "💰 Add points\n"
            "📞 Private calls 🔥",
            reply_markup=menu(t)
        )

    elif text == t["model"]:

        await update.message.reply_text(
            "🔥💋 MODEL MODE 💋🔥\n\n"
            "👤 My profile\n"
            "📸 My content\n"
            "💰 My earnings\n"
            "📞 My calls\n"
            "💸 Withdraw",
            reply_markup=menu(t)
        )

    elif text == t["agency"]:

        await update.message.reply_text(
            "🏢🔥 AGENCY MODE 🔥🏢\n\n"
            "👩‍👩‍👧 My Muses\n"
            "➕ Recruit\n"
            "🔑 Agency codes\n"
            "📊 Team sales\n"
            "💰 Commissions",
            reply_markup=menu(t)
        )

def main():

    Thread(
        target=run_web,
        daemon=True
    ).start()

    bot = Application.builder().token(TOKEN).build()

    bot.add_handler(
        CommandHandler("start", start)
    )

    bot.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            messages
        )
    )

    print("🖤🔥 Velvet Musa iniciado 😈")

    bot.run_polling()

if __name__ == "__main__":
    main()
