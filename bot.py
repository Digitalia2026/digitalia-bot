import os
from threading import Thread

from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

# =========================================================
# 🌐 CANALES
# =========================================================

MODELS_CHANNEL = "https://t.me/TU_CANAL_DE_MODELOS"
AGENCY_CHANNEL = "https://t.me/TU_CANAL_DE_AGENCIAS"

# =========================================================
# 🌐 SERVIDOR PARA RENDER
# =========================================================

web = Flask(__name__)

@web.route("/")
def home():
    return "🖤🔥 Velvet Musa funcionando 😈"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    web.run(host="0.0.0.0", port=port)

# =========================================================
# 🌎 TEXTOS
# =========================================================

ES = {
    "home": "🏠 Inicio",
    "user": "👤 Soy Usuario 😏",
    "model": "🔥 Soy Modelo 💋",
    "agency": "🏢 Soy Agencia 😈",
    "language": "🌎 Idioma",

    "welcome": """🖤🔥 VELVET MUSA 🔥🖤

🌙 Hay noches que empiezan con un simple “hola”… 😈

💋 Conoce a nuestras Musas
✨ Elige la que despierte tu curiosidad
💬 Habla con ella
📸 Descubre su contenido privado
📞 Comparte un momento a solas 🔥

😈 Quizás encuentres exactamente lo que estabas buscando…

👇 ¿Qué estás buscando?""",

    "choose": "👇 Elige una opción:",
    "back": "⬅️ Volver",

    "user_title": "👤💎 MODO USUARIO 💎",
    "explore": "🔎 Explorar Musas",
    "balance": "⭐ Mi saldo",
    "recharge": "💰 Recargar saldo",
    "purchases": "🛍️ Mis compras",
    "calls": "📞 Mis llamadas",
    "profile": "👤 Mi perfil",

    "model_title": "🔥💎 MODO MODELO 💎🔥",
    "my_profile": "👤 Mi perfil",
    "content": "📸 Mi contenido",
    "publish": "➕ Publicar contenido",
    "earnings": "💰 Mis ganancias",
    "sales": "📊 Mis ventas",
    "model_calls": "📞 Mis llamadas",
    "my_agency": "🏢 Mi agencia",
    "withdraw": "💸 Solicitar retiro",
    "model_channel": "📢 Canal exclusivo para Musas",

    "agency_title": "🏢🔥 MODO AGENCIA 🔥🏢",
    "models": "👩‍👩‍👧 Mis Musas",
    "recruit": "➕ Reclutar Musa",
    "codes": "🔑 Mis códigos",
    "team_sales": "📊 Ventas del equipo",
    "commissions": "💰 Mis comisiones",
    "agency_withdraw": "💸 Solicitar retiro",
    "agency_profile": "📝 Mi agencia",
    "create_agency": "🏗️ Crear agencia",
    "agency_channel": "📢 Canal exclusivo para agencias",

    "language_title": "🌎 IDIOMA / LANGUAGE",
    "language_text": "Elige el idioma de Velvet Musa:",
    "spanish": "🇪🇸 Español",
    "english": "🇺🇸 English",

    "catalog": "🔥 DESCUBRE NUESTRAS MUSAS 🔥",
    "view_profile": "💋 Ver perfil",
    "previous": "⬅️ Anterior",
    "next": "Siguiente ➡️",

    "ana": """👩🔥 ANA 🔥

🎂 24 años · 🇨🇴 Colombia

✨ Me encanta conversar, conocer personas y compartir momentos especiales. 😈

🟢 Disponible

📞 Llamadas desde 25 💎/min
📸 Contenido desde 300 💎""",

    "locked": """📸🔥 CONTENIDO EXCLUSIVO 🔥

🔒 Las fotos y vídeos privados estarán disponibles mediante puntos. 💎

😈 Esta función estará disponible próximamente.""",

    "balance_text": """⭐💎 MI SALDO 💎⭐

💎 Saldo disponible: 0 puntos

🔥 Próximamente podrás recargar y disfrutar de contenido exclusivo.""",

    "coming": """🚀🔥 PRÓXIMAMENTE 🔥

Estamos preparando esta función para Velvet Musa. 🖤😈"""
}


EN = {
    "home": "🏠 Home",
    "user": "👤 I'm a User 😏",
    "model": "🔥 I'm a Model 💋",
    "agency": "🏢 I'm an Agency 😈",
    "language": "🌎 Language",

    "welcome": """🖤🔥 VELVET MUSA 🔥🖤

🌙 Some nights start with a simple “hello”… 😈

💋 Meet our Muses
✨ Choose the one who catches your eye
💬 Talk to her
📸 Discover her private content
📞 Spend some private time together 🔥

😈 You might find exactly what you've been looking for…

👇 What are you looking for?""",

    "choose": "👇 Choose an option:",
    "back": "⬅️ Back",

    "user_title": "👤💎 USER MODE 💎",
    "explore": "🔎 Explore Muses",
    "balance": "⭐ My balance",
    "recharge": "💰 Add balance",
    "purchases": "🛍️ My purchases",
    "calls": "📞 My calls",
    "profile": "👤 My profile",

    "model_title": "🔥💎 MODEL MODE 💎🔥",
    "my_profile": "👤 My profile",
    "content": "📸 My content",
    "publish": "➕ Publish content",
    "earnings": "💰 My earnings",
    "sales": "📊 My sales",
    "model_calls": "📞 My calls",
    "my_agency": "🏢 My agency",
    "withdraw": "💸 Request withdrawal",
    "model_channel": "📢 Exclusive Muses channel",

    "agency_title": "🏢🔥 AGENCY MODE 🔥🏢",
    "models": "👩‍👩‍👧 My Muses",
    "recruit": "➕ Recruit a Muse",
    "codes": "🔑 My codes",
    "team_sales": "📊 Team sales",
    "commissions": "💰 My commissions",
    "agency_withdraw": "💸 Request withdrawal",
    "agency_profile": "📝 My agency",
    "create_agency": "🏗️ Create agency",
    "agency_channel": "📢 Exclusive agency channel",

    "language_title": "🌎 LANGUAGE / IDIOMA",
    "language_text": "Choose your Velvet Musa language:",
    "spanish": "🇪🇸 Español",
    "english": "🇺🇸 English",

    "catalog": "🔥 DISCOVER OUR MUSES 🔥",
    "view_profile": "💋 View profile",
    "previous": "⬅️ Previous",
    "next": "Next ➡️",

    "ana": """👩🔥 ANA 🔥

🎂 24 years · 🇨🇴 Colombia

✨ I love talking, meeting new people and sharing special moments. 😈

🟢 Available

📞 Calls from 25 💎/min
📸 Content from 300 💎""",

    "locked": """📸🔥 PRIVATE CONTENT 🔥

🔒 Private photos and videos will be available using points. 💎

😈 This feature will be available soon.""",

    "balance_text": """⭐💎 MY BALANCE 💎⭐

💎 Available balance: 0 points

🔥 Soon you'll be able to add points and enjoy exclusive content.""",

    "coming": """🚀🔥 COMING SOON 🔥

We're preparing this feature for Velvet Musa. 🖤😈"""
}

# =========================================================
# 🌎 IDIOMA
# =========================================================

def get_lang(context):
    return context.user_data.get("lang", "es")

def texts(context):
    return ES if get_lang(context) == "es" else EN

def detect_language(update):
    code = update.effective_user.language_code or "es"
    return "en" if code.lower().startswith("en") else "es"

# =========================================================
# 📱 MENÚ INFERIOR
# =========================================================

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

# =========================================================
# 🏠 MENÚ PRINCIPAL
# =========================================================

def main_menu(t):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t["user"], callback_data="user")],
        [InlineKeyboardButton(t["model"], callback_data="model")],
        [InlineKeyboardButton(t["agency"], callback_data="agency")],
        [InlineKeyboardButton(t["language"], callback_data="language")]
    ])

# =========================================================
# 👤 MENÚ USUARIO
# =========================================================

def user_menu(t):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t["explore"], callback_data="explore")],
        [InlineKeyboardButton(t["balance"], callback_data="balance")],
        [InlineKeyboardButton(t["recharge"], callback_data="recharge")],
        [InlineKeyboardButton(t["purchases"], callback_data="purchases")],
        [InlineKeyboardButton(t["calls"], callback_data="calls")],
        [InlineKeyboardButton(t["profile"], callback_data="user_profile")]
    ])

# =========================================================
# 🔥 MENÚ MODELO
# =========================================================

def model_menu(t):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t["my_profile"], callback_data="model_profile")],
        [InlineKeyboardButton(t["content"], callback_data="model_content")],
        [InlineKeyboardButton(t["publish"], callback_data="publish")],
        [InlineKeyboardButton(t["earnings"], callback_data="earnings")],
        [InlineKeyboardButton(t["sales"], callback_data="sales")],
        [InlineKeyboardButton(t["model_calls"], callback_data="model_calls")],
        [InlineKeyboardButton(t["my_agency"], callback_data="my_agency")],
        [InlineKeyboardButton(t["withdraw"], callback_data="withdraw")],
        [InlineKeyboardButton(t["model_channel"], url=MODELS_CHANNEL)],
        [InlineKeyboardButton(t["back"], callback_data="home")]
    ])

# =========================================================
# 🏢 MENÚ AGENCIA
# =========================================================

def agency_menu(t):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t["models"], callback_data="models")],
        [InlineKeyboardButton(t["recruit"], callback_data="recruit")],
        [InlineKeyboardButton(t["codes"], callback_data="codes")],
        [InlineKeyboardButton(t["team_sales"], callback_data="team_sales")],
        [InlineKeyboardButton(t["commissions"], callback_data="commissions")],
        [InlineKeyboardButton(t["agency_withdraw"], callback_data="agency_withdraw")],
        [InlineKeyboardButton(t["agency_profile"], callback_data="agency_profile")],
        [InlineKeyboardButton(t["create_agency"], callback_data="create_agency")],
        [InlineKeyboardButton(t["agency_channel"], url=AGENCY_CHANNEL)],
        [InlineKeyboardButton(t["back"], callback_data="home")]
    ])

# =========================================================
# 🌎 IDIOMA
# =========================================================

def language_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🇪🇸 Español", callback_data="lang_es")],
        [InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")]
    ])

# =========================================================
# ▶️ START
# =========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "lang" not in context.user_data:
        context.user_data["lang"] = detect_language(update)

    t = texts(context)

    await update.message.reply_text(
        t["welcome"],
        reply_markup=bottom_menu(t)
    )

    await update.message.reply_text(
        t["choose"],
        reply_markup=main_menu(t)
    )

# =========================================================
# 📱 MENÚ INFERIOR
# =========================================================

async def text_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = texts(context)
    text = update.message.text

    if text == t["home"]:
        await update.message.reply_text(
            t["welcome"],
            reply_markup=bottom_menu(t)
        )
        await update.message.reply_text(
            t["choose"],
            reply_markup=main_menu(t)
        )

    elif text == t["user"]:
        await update.message.reply_text(
            t["user_title"],
            reply_markup=user_menu(t)
        )

    elif text == t["model"]:
        await update.message.reply_text(
            t["model_title"],
            reply_markup=model_menu(t)
        )

    elif text == t["agency"]:
        await update.message.reply_text(
            t["agency_title"],
            reply_markup=agency_menu(t)
        )

    elif text == t["language"]:
        await update.message.reply_text(
            t["language_text"],
            reply_markup=language_menu()
        )

# =========================================================
# 🔘 BOTONES
# =========================================================

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    t = texts(context)
    data = query.data

    if data == "lang_es":
        context.user_data["lang"] = "es"
        t = ES

        await query.edit_message_text(
            t["welcome"],
            reply_markup=main_menu(t)
        )
        return

    if data == "lang_en":
        context.user_data["lang"] = "en"
        t = EN

        await query.edit_message_text(
            t["welcome"],
            reply_markup=main_menu(t)
        )
        return

    if data == "language":
        await query.edit_message_text(
            t["language_text"],
            reply_markup=language_menu()
        )
        return

    if data == "home":
        await query.edit_message_text(
            t["welcome"],
            reply_markup=main_menu(t)
        )
        return

    if data == "user":
        await query.edit_message_text(
            t["user_title"],
            reply_markup=user_menu(t)
        )
        return

    if data == "model":
        await query.edit_message_text(
            t["model_title"],
            reply_markup=model_menu(t)
        )
        return

    if data == "agency":
        await query.edit_message_text(
            t["agency_title"],
            reply_markup=agency_menu(t)
        )
        return

    if data == "explore":
        await query.edit_message_text(
            t["catalog"] + "\n\n"
            "📸 👩 Ana, 24 🇨🇴\n\n"
            "✨ Me encanta conversar y compartir momentos especiales. 😈\n\n"
            "🟢 Disponible\n"
            "📞 25 💎/min\n"
            "📸 Contenido desde 300 💎",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(t["view_profile"], callback_data="ana")],
                [
                    InlineKeyboardButton(t["previous"], callback_data="soon"),
                    InlineKeyboardButton(t["next"], callback_data="soon")
                ],
                [InlineKeyboardButton(t["back"], callback_data="user")]
            ])
        )
        return

    if data == "ana":
        await query.edit_message_text(
            t["ana"],
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(
                    "📸 " + ("Ver contenido exclusivo" if get_lang(context) == "es" else "View private content"),
                    callback_data="ana_content"
                )],
                [InlineKeyboardButton(
                    "📞 " + ("Solicitar llamada" if get_lang(context) == "es" else "Request a call"),
                    callback_data="ana_call"
                )],
                [InlineKeyboardButton(t["back"], callback_data="explore")]
            ])
        )
        return

    if data == "ana_content":
        await query.edit_message_text(
            t["locked"],
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(t["recharge"], callback_data="recharge")],
                [InlineKeyboardButton(t["back"], callback_data="ana")]
            ])
        )
        return

    if data == "ana_call":
        message = (
            "📞🔥 LLAMADA PRIVADA 🔥\n\n"
            "👩 Ana\n\n"
            "💎 25 puntos por minuto\n\n"
            "😈 Esta función estará disponible próximamente."
            if get_lang(context) == "es"
            else
            "📞🔥 PRIVATE CALL 🔥\n\n"
            "👩 Ana\n\n"
            "💎 25 points per minute\n\n"
            "😈 This feature will be available soon."
        )

        await query.edit_message_text(
            message,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(t["back"], callback_data="ana")]
            ])
        )
        return

    if data == "balance":
        await query.edit_message_text(
            t["balance_text"],
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(t["recharge"], callback_data="recharge")],
                [InlineKeyboardButton(t["back"], callback_data="user")]
            ])
        )
        return

    if data == "recharge":
        await query.edit_message_text(
            t["coming"],
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(t["back"], callback_data="user")]
            ])
        )
        return

    if data in ["purchases", "calls", "user_profile"]:
        await query.edit_message_text(
            t["coming"],
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(t["back"], callback_data="user")]
            ])
        )
        return

    if data in [
        "model_profile",
        "model_content",
        "publish",
        "earnings",
        "sales",
        "model_calls",
        "my_agency",
        "withdraw"
    ]:
        await query.edit_message_text(
            t["coming"],
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(t["back"], callback_data="model")]
            ])
        )
        return

    if data in [
        "models",
        "recruit",
        "codes",
        "team_sales",
        "commissions",
        "agency_withdraw",
        "agency_profile",
        "create_agency"
    ]:
        await query.edit_message_text(
            t["coming"],
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(t["back"], callback_data="agency")]
            ])
        )
        return

    if data == "soon":
        message = (
            "🔥 Pronto tendremos más Musas disponibles. 😈"
            if get_lang(context) == "es"
            else
            "🔥 More Muses will be available soon. 😈"
        )

        await query.answer(message, show_alert=True)

# =========================================================
# 🚀 INICIAR
# =========================================================

def main():
    Thread(target=run_web, daemon=True).start()

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(buttons))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, text_menu)
    )

    print("🖤🔥 Velvet Musa iniciado 😈")

    application.run_polling()

if __name__ == "__main__":
    main()
```
