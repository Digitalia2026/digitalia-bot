import os
from threading import Thread

from flask import Flask
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")

# =========================================================
# 🌐 CONFIGURACIÓN DE CANALES
# =========================================================

MODELS_CHANNEL = "https://t.me/TU_CANAL_DE_MODELOS"
AGENCY_CHANNEL = "https://t.me/TU_CANAL_DE_AGENCIAS"


# =========================================================
# 🌐 SERVIDOR WEB PARA RENDER
# =========================================================

app_web = Flask(__name__)


@app_web.route("/")
def inicio_web():
    return "🖤🔥 Velvet Musa está funcionando 😈"


def iniciar_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host="0.0.0.0", port=port)


# =========================================================
# 🌎 IDIOMAS
# =========================================================

TEXTOS = {

    "es": {

        "user": "👤 Soy Usuario",
        "model": "🔥 Soy Modelo",
        "agency": "🏢 Soy Agencia",
        "home": "🏠 Inicio",
        "language": "🌎 Idioma",

        "welcome": (
            "🖤🔥 VELVET MUSA 🔥🖤\n\n"
            "🌙 Hay noches que empiezan con un simple “hola”… 😈\n\n"
            "💋 Conoce a nuestras Musas\n"
            "✨ Elige la que despierte tu curiosidad\n"
            "💬 Habla con ella\n"
            "📸 Descubre su contenido privado\n"
            "📞 Comparte un momento a solas 🔥\n\n"
            "😈 Quizás encuentres exactamente lo que estabas buscando…\n\n"
            "👇 ¿Qué estás buscando?"
        ),

        "again": (
            "🖤🔥 ¡Qué bueno verte otra vez! 😈\n\n"
            "🌙 ¿Qué quieres hacer esta noche?"
        ),

        "choose": "👇 Selecciona una opción:",

        "user_title": "👤💎 MODO USUARIO 💎",
        "user_text": (
            "🔎 Explora nuestras Musas\n"
            "⭐ Consulta tu saldo\n"
            "💰 Recarga puntos\n"
            "🛍️ Revisa tus compras\n"
            "📞 Gestiona tus llamadas"
        ),

        "explore": "🔎 Explorar Musas",
        "balance": "⭐ Mi saldo",
        "recharge": "💰 Recargar saldo",
        "purchases": "🛍️ Mis compras",
        "calls": "📞 Mis llamadas",
        "profile": "👤 Mi perfil",

        "model_title": "🔥💎 MODO MODELO 💎🔥",
        "model_text": (
            "📸 Publica tu contenido\n"
            "💬 Conecta con usuarios\n"
            "📞 Recibe llamadas\n"
            "💰 Controla tus ganancias\n"
            "📊 Revisa tus ventas\n"
            "💸 Solicita tus retiros"
        ),

        "my_profile": "👤 Mi perfil",
        "my_content": "📸 Mi contenido",
        "publish": "➕ Publicar contenido",
        "earnings": "💰 Mis ganancias",
        "sales": "📊 Mis ventas",
        "model_calls": "📞 Mis llamadas",
        "my_agency": "🏢 Mi agencia",
        "withdraw": "💸 Solicitar retiro",
        "model_channel": "📢 Canal exclusivo para Musas",

        "agency_title": "🏢🔥 MODO AGENCIA 🔥🏢",
        "agency_text": (
            "👩‍👩‍👧 Gestiona tus Musas\n"
            "➕ Recluta nuevas modelos\n"
            "🔑 Administra tus códigos\n"
            "📊 Controla las ventas\n"
            "💰 Consulta tus comisiones\n"
            "💸 Gestiona tus retiros"
        ),

        "my_models": "👩‍👩‍👧 Mis Musas",
        "recruit": "➕ Reclutar Musa",
        "codes": "🔑 Mis códigos",
        "team_sales": "📊 Ventas del equipo",
        "commissions": "💰 Mis comisiones",
        "agency_withdraw": "💸 Solicitar retiro",
        "agency_profile": "📝 Mi agencia",
        "create_agency": "🏗️ Crear agencia",
        "agency_channel": "📢 Canal exclusivo para agencias",

        "back": "⬅️ Volver",
        "available": "🟢 Disponible",
        "see_profile": "💋 Ver perfil",
        "previous": "⬅️ Anterior",
        "next": "Siguiente ➡️",

        "language_title": "🌎 IDIOMA / LANGUAGE",
        "language_text": "Elige el idioma de Velvet Musa:",

        "spanish": "🇪🇸 Español",
        "english": "🇺🇸 English",

        "models_title": "🔥 DESCUBRE NUESTRAS MUSAS 🔥",

        "ana_profile": (
            "👩🔥 ANA 🔥\n\n"
            "🎂 24 años · 🇨🇴 Colombia\n\n"
            "✨ Me encanta conversar, conocer personas "
            "y compartir momentos especiales. 😈\n\n"
            "🟢 Disponible\n\n"
            "📞 Llamadas desde 25 💎/min\n"
            "📸 Contenido desde 300 💎"
        ),

        "content_locked": (
            "📸🔥 CONTENIDO EXCLUSIVO 🔥\n\n"
            "🔒 El contenido se desbloquea utilizando "
            "tus puntos de Velvet Musa. 💎\n\n"
            "🚀 Sistema de puntos próximamente."
        ),

        "balance_text": (
            "⭐💎 MI SALDO 💎⭐\n\n"
            "💎 Saldo disponible: 0 puntos\n\n"
            "🔥 Recarga para comenzar a descubrir "
            "contenido exclusivo."
        ),

        "recharge_text": (
            "💰🔥 RECARGAR SALDO 🔥💰\n\n"
            "💎 Próximamente podrás comprar puntos "
            "para desbloquear contenido y disfrutar "
            "de llamadas privadas. 😈"
        ),

        "coming": (
            "🚀🔥 FUNCIÓN EN DESARROLLO 🔥\n\n"
            "Estamos preparando esta función para "
            "Velvet Musa. 🖤"
        ),
    },

    "en": {

        "user": "👤 I'm a User",
        "model": "🔥 I'm a Model",
        "agency": "🏢 I'm an Agency",
        "home": "🏠 Home",
        "language": "🌎 Language",

        "welcome": (
            "🖤🔥 VELVET MUSA 🔥🖤\n\n"
            "🌙 Some nights start with a simple “hello”… 😈\n\n"
            "💋 Meet our Muses\n"
            "✨ Choose the one who catches your eye\n"
            "💬 Talk to her\n"
            "📸 Discover her private content\n"
            "📞 Spend some private time together 🔥\n\n"
            "😈 You might find exactly what you've been looking for…\n\n"
            "👇 What are you looking for?"
        ),

        "again": (
            "🖤🔥 Good to see you again! 😈\n\n"
            "🌙 What would you like to do tonight?"
        ),

        "choose": "👇 Choose an option:",

        "user_title": "👤💎 USER MODE 💎",
        "user_text": (
            "🔎 Explore our Muses\n"
            "⭐ Check your balance\n"
            "💰 Add points\n"
            "🛍️ View your purchases\n"
            "📞 Manage your calls"
        ),

        "explore": "🔎 Explore Muses",
        "balance": "⭐ My balance",
        "recharge": "💰 Add balance",
        "purchases": "🛍️ My purchases",
        "calls": "📞 My calls",
        "profile": "👤 My profile",

        "model_title": "🔥💎 MODEL MODE 💎🔥",
        "model_text": (
            "📸 Publish your content\n"
            "💬 Connect with users\n"
            "📞 Receive calls\n"
            "💰 Manage your earnings\n"
            "📊 Check your sales\n"
            "💸 Request withdrawals"
        ),

        "my_profile": "👤 My profile",
        "my_content": "📸 My content",
        "publish": "➕ Publish content",
        "earnings": "💰 My earnings",
        "sales": "📊 My sales",
        "model_calls": "📞 My calls",
        "my_agency": "🏢 My agency",
        "withdraw": "💸 Request withdrawal",
        "model_channel": "📢 Exclusive Muses channel",

        "agency_title": "🏢🔥 AGENCY MODE 🔥🏢",
        "agency_text": (
            "👩‍👩‍👧 Manage your Muses\n"
            "➕ Recruit new models\n"
            "🔑 Manage your codes\n"
            "📊 Track team sales\n"
            "💰 Check your commissions\n"
            "💸 Manage withdrawals"
        ),

        "my_models": "👩‍👩‍👧 My Muses",
        "recruit": "➕ Recruit a Muse",
        "codes": "🔑 My codes",
        "team_sales": "📊 Team sales",
        "commissions": "💰 My commissions",
        "agency_withdraw": "💸 Request withdrawal",
        "agency_profile": "📝 My agency",
        "create_agency": "🏗️ Create agency",
        "agency_channel": "📢 Exclusive agency channel",

        "back": "⬅️ Back",
        "available": "🟢 Available",
        "see_profile": "💋 View profile",
        "previous": "⬅️ Previous",
        "next": "Next ➡️",

        "language_title": "🌎 LANGUAGE / IDIOMA",
        "language_text": "Choose your Velvet Musa language:",

        "spanish": "🇪🇸 Español",
        "english": "🇺🇸 English",

        "models_title": "🔥 DISCOVER OUR MUSES 🔥",

        "ana_profile": (
            "👩🔥 ANA 🔥\n\n"
            "🎂 24 years · 🇨🇴 Colombia\n\n"
            "✨ I love talking, meeting new people "
            "and sharing special moments. 😈\n\n"
            "🟢 Available\n\n"
            "📞 Calls from 25 💎/min\n"
            "📸 Content from 300 💎"
        ),

        "content_locked": (
            "📸🔥 PRIVATE CONTENT 🔥\n\n"
            "🔒 Content will be unlocked using "
            "your Velvet Musa points. 💎\n\n"
            "🚀 Points system coming soon."
        ),

        "balance_text": (
            "⭐💎 MY BALANCE 💎⭐\n\n"
            "💎 Available balance: 0 points\n\n"
            "🔥 Add points to start discovering "
            "exclusive content."
        ),

        "recharge_text": (
            "💰🔥 ADD BALANCE 🔥💰\n\n"
            "💎 Soon you'll be able to purchase points "
            "to unlock content and enjoy private calls. 😈"
        ),

        "coming": (
            "🚀🔥 FEATURE IN DEVELOPMENT 🔥\n\n"
            "We're preparing this feature for "
            "Velvet Musa. 🖤"
        ),
    }
}


# =========================================================
# 🧠 IDIOMA DEL USUARIO
# =========================================================

def idioma_usuario(update: Update):

    user = update.effective_user

    if user.language_code:
        codigo = user.language_code.lower()

        if codigo.startswith("es"):
            return "es"

        if codigo.startswith("en"):
            return "en"

    return "es"


def get_lang(context):

    return context.user_data.get("language", "es")


# =========================================================
# 📱 MENÚ INFERIOR
# =========================================================

def menu_inferior(lang):

    t = TEXTOS[lang]

    return ReplyKeyboardMarkup(
        [
            [t["home"], t["user"]],
            [t["model"], t["agency"]],
            [t["language"]],
        ],
        resize_keyboard=True,
        is_persistent=True
    )


# =========================================================
# 🌟 MENÚ PRINCIPAL
# =========================================================

def menu_principal(lang):

    t = TEXTOS[lang]

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                t["user"],
                callback_data="usuario"
            )
        ],
        [
            InlineKeyboardButton(
                t["model"],
                callback_data="modelo"
            )
        ],
        [
            InlineKeyboardButton(
                t["agency"],
                callback_data="agencia"
            )
        ],
        [
            InlineKeyboardButton(
                t["language"],
                callback_data="idioma"
            )
        ]
    ])


# =========================================================
# 👤 MENÚ USUARIO
# =========================================================

def menu_usuario(lang):

    t = TEXTOS[lang]

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                t["explore"],
                callback_data="explorar"
            )
        ],
        [
            InlineKeyboardButton(
                t["balance"],
                callback_data="saldo"
            )
        ],
        [
            InlineKeyboardButton(
                t["recharge"],
                callback_data="recargar"
            )
        ],
        [
            InlineKeyboardButton(
                t["purchases"],
                callback_data="compras"
            )
        ],
        [
            InlineKeyboardButton(
                t["calls"],
                callback_data="mis_llamadas"
            )
        ],
        [
            InlineKeyboardButton(
                t["profile"],
                callback_data="perfil"
            )
        ]
    ])


# =========================================================
# 🔥 MENÚ MODELO
# =========================================================

def menu_modelo(lang):

    t = TEXTOS[lang]

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                t["my_profile"],
                callback_data="perfil_modelo"
            )
        ],
        [
            InlineKeyboardButton(
                t["my_content"],
                callback_data="contenido_modelo"
            )
        ],
        [
            InlineKeyboardButton(
                t["publish"],
                callback_data="publicar"
            )
        ],
        [
            InlineKeyboardButton(
                t["earnings"],
                callback_data="ganancias"
            )
        ],
        [
            InlineKeyboardButton(
                t["sales"],
                callback_data="ventas"
            )
        ],
        [
            InlineKeyboardButton(
                t["model_calls"],
                callback_data="llamadas_modelo"
            )
        ],
        [
            InlineKeyboardButton(
                t["my_agency"],
                callback_data="mi_agencia"
            )
        ],
        [
            InlineKeyboardButton(
                t["withdraw"],
                callback_data="retiro"
            )
        ],
        [
            InlineKeyboardButton(
                t["model_channel"],
                url=MODELS_CHANNEL
            )
        ]
    ])


# =========================================================
# 🏢 MENÚ AGENCIA
# =========================================================

def menu_agencia(lang):

    t = TEXTOS[lang]

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                t["my_models"],
                callback_data="mis_modelos"
            )
        ],
        [
            InlineKeyboardButton(
                t["recruit"],
                callback_data="reclutar"
            )
        ],
        [
            InlineKeyboardButton(
                t["codes"],
                callback_data="codigos"
            )
        ],
        [
            InlineKeyboardButton(
                t["team_sales"],
                callback_data="ventas_equipo"
            )
        ],
        [
            InlineKeyboardButton(
                t["commissions"],
                callback_data="comisiones"
            )
        ],
        [
            InlineKeyboardButton(
                t["agency_withdraw"],
                callback_data="retiro_agencia"
            )
        ],
        [
            InlineKeyboardButton(
                t["agency_profile"],
                callback_data="perfil_agencia"
            )
        ],
        [
            InlineKeyboardButton(
                t["create_agency"],
                callback_data="crear_agencia"
            )
        ],
        [
            InlineKeyboardButton(
                t["agency_channel"],
                url=AGENCY_CHANNEL
            )
        ]
    ])


# =========================================================
# 🌎 MENÚ DE IDIOMA
# =========================================================

def menu_idioma():

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🇪🇸 Español",
                callback_data="lang_es"
            )
        ],
        [
            InlineKeyboardButton(
                "🇺🇸 English",
                callback_data="lang_en"
            )
        ]
    ])


# =========================================================
# 👋 START
# =========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Detectamos el idioma automáticamente
    if "language" not in context.user_data:
        context.user_data["language"] = idioma_usuario(update)
        primera_vez = True
    else:
        primera_vez = False

    lang = get_lang(context)
    t = TEXTOS[lang]

    if primera_vez:

        await update.message.reply_text(
            t["welcome"],
            reply_markup=menu_inferior(lang)
        )

    else:

        await update.message.reply_text(
            t["again"],
            reply_markup=menu_inferior(lang)
        )

    await update.message.reply_text(
        t["choose"],
        reply_markup=menu_principal(lang)
    )


# =========================================================
# 📱 BOTONES DEL MENÚ INFERIOR
# =========================================================

async def menu_texto(update: Update, context: ContextTypes.DEFAULT_TYPE):

    texto = update.message.text
    lang = get_lang(context)
    t = TEXTOS[lang]

    # 🏠 INICIO

    if texto == t["home"]:

        await update.message.reply_text(
            t["again"],
            reply_markup=menu_inferior(lang)
        )

        await update.message.reply_text(
            t["choose"],
            reply_markup=menu_principal(lang)
        )

    # 👤 USUARIO

    elif texto == t["user"]:

        await update.message.reply_text(
            f"{t['user_title']}\n\n"
            f"{t['user_text']}\n\n"
            f"{t['choose']}",
            reply_markup=menu_usuario(lang)
        )

    # 🔥 MODELO

    elif texto == t["model"]:

        await update.message.reply_text(
            f"{t['model_title']}\n\n"
            f"{t['model_text']}\n\n"
            f"{t['choose']}",
            reply_markup=menu_modelo(lang)
        )

    # 🏢 AGENCIA

    elif texto == t["agency"]:

        await update.message.reply_text(
            f"{t['agency_title']}\n\n"
            f"{t['agency_text']}\n\n"
            f"{t['choose']}",
            reply_markup=menu_agencia(lang)
        )

    # 🌎 IDIOMA

    elif texto == t["language"]:

        await update.message.reply_text(
            f"{t['language_title']}\n\n"
            f"{t['language_text']}",
            reply_markup=menu_idioma()
        )


# =========================================================
# 🔘 BOTONES INTERNOS
# =========================================================

async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    lang = get_lang(context)
    t = TEXTOS[lang]

    # =====================================================
    # 🌎 CAMBIAR IDIOMA
    # =====================================================

    if query.data == "idioma":

        await query.edit_message_text(
            f"{t['language_title']}\n\n"
            f"{t['language_text']}",
            reply_markup=menu_idioma()
        )

        return

    if query.data == "lang_es":

        context.user_data["language"] = "es"

        t = TEXTOS["es"]

        await query.edit_message_text(
            t["welcome"],
            reply_markup=menu_principal("es")
        )

        return

    if query.data == "lang_en":

        context.user_data["language"] = "en"

        t = TEXTOS["en"]

        await query.edit_message_text(
            t["welcome"],
            reply_markup=menu_principal("en")
        )

        return

    # =====================================================
    # 👤 USUARIO
    # =====================================================

    if query.data == "usuario":

        await query.edit_message_text(
            f"{t['user_title']}\n\n"
            f"{t['user_text']}\n\n"
            f"{t['choose']}",
            reply_markup=menu_usuario(lang)
       
