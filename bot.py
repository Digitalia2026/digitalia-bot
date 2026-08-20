import os
import sqlite3
from threading import Thread

from flask import Flask
from telegram import Update, ReplyKeyboardMarkup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler
from telegram.ext import MessageHandler, CallbackQueryHandler
from telegram.ext import ContextTypes, filters


TOKEN = os.getenv("BOT_TOKEN")

# =========================================================
# CONFIGURACIÓN
# =========================================================

MELISSA_PHOTO_URL = (
    "https://i.ibb.co/VYpN8wtP/"
    "Chat-GPT-Image-1-ago-2026-06-35-15-p-m.png"
)

MODELS_CHANNEL = "https://t.me/+BUxwqByLYK00ZTYx"
AGENCY_CHANNEL = "https://t.me/+MrTIOV4GlqAzNWIx"

DB_FILE = "velvet_musa.db"


# =========================================================
# BASE DE DATOS
# =========================================================

def db_connect():
    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row
    return connection


def init_database():
    connection = db_connect()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS models (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE NOT NULL,
            artistic_name TEXT NOT NULL,
            velvet_username TEXT UNIQUE NOT NULL,
            photo_file_id TEXT,
            description TEXT,
            chat_enabled INTEGER DEFAULT 0,
            chat_price INTEGER DEFAULT 1,
            photos_enabled INTEGER DEFAULT 0,
            photos_price INTEGER DEFAULT 20,
            videos_enabled INTEGER DEFAULT 0,
            videos_price INTEGER DEFAULT 50,
            calls_enabled INTEGER DEFAULT 0,
            calls_price INTEGER DEFAULT 25,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    connection.commit()
    connection.close()


def username_available(username, telegram_id):
    username = username.lower().replace("@", "").strip()

    connection = db_connect()

    row = connection.execute(
        """
        SELECT telegram_id
        FROM models
        WHERE velvet_username = ?
        """,
        (username,)
    ).fetchone()

    connection.close()

    if row is None:
        return True

    return row["telegram_id"] == telegram_id


def save_model(telegram_id, data):
    connection = db_connect()

    connection.execute(
        """
        INSERT OR REPLACE INTO models (
            telegram_id,
            artistic_name,
            velvet_username,
            photo_file_id,
            description,
            chat_enabled,
            chat_price,
            photos_enabled,
            photos_price,
            videos_enabled,
            videos_price,
            calls_enabled,
            calls_price
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            telegram_id,
            data["artistic_name"],
            data["velvet_username"],
            data.get("photo_file_id"),
            data.get("description", ""),
            int(data["chat_enabled"]),
            int(data["chat_price"]),
            int(data["photos_enabled"]),
            int(data["photos_price"]),
            int(data["videos_enabled"]),
            int(data["videos_price"]),
            int(data["calls_enabled"]),
            int(data["calls_price"])
        )
    )

    connection.commit()
    connection.close()


def get_model_by_telegram_id(telegram_id):
    connection = db_connect()

    row = connection.execute(
        """
        SELECT *
        FROM models
        WHERE telegram_id = ?
        """,
        (telegram_id,)
    ).fetchone()

    connection.close()

    return row


def get_model_by_username(username):
    username = username.lower().replace("@", "").strip()

    connection = db_connect()

    row = connection.execute(
        """
        SELECT *
        FROM models
        WHERE velvet_username = ?
        """,
        (username,)
    ).fetchone()

    connection.close()

    return row


def get_all_models():
    connection = db_connect()

    rows = connection.execute(
        """
        SELECT *
        FROM models
        ORDER BY created_at ASC
        """
    ).fetchall()

    connection.close()

    return rows


# =========================================================
# SERVIDOR PARA RENDER
# =========================================================

web = Flask(__name__)


@web.route("/")
def home():
    return "🖤🔥 Velvet Musa funcionando 😈"


def run_web():
    port = int(os.environ.get("PORT", 10000))

    web.run(
        host="0.0.0.0",
        port=port
    )


# =========================================================
# TEXTOS ESPAÑOL
# =========================================================

ES = {
    "home": "🏠 Inicio",
    "user": "👤 Soy Usuario 😏",
    "model": "🔥 Soy Modelo 💋",
    "agency": "🏢 Soy Agencia 😈",
    "language": "🌎 Idioma",

    "welcome": (
        "🖤🔥 VELVET MUSA 🔥🖤\n\n"
        "🌙 Hay noches que empiezan con un simple «hola»… 😈\n\n"
        "💋 Conoce nuestras Musas\n"
        "✨ Elige la que despierte tu curiosidad\n"
        "💬 Habla con ella\n"
        "📸 Descubre contenido exclusivo\n"
        "📞 Comparte un momento a solas 🔥\n\n"
        "😈 Quizás encuentres exactamente lo que estabas buscando…\n\n"
        "👇 Elige una opción:"
    ),

    "user_title": "👤💎 MODO USUARIO 💎👤",

    "explore": "🔎 Explorar Musas",
    "balance": "⭐ Mi saldo",
    "recharge": "💰 Recargar saldo",
    "history": "📜 Historial",
    "calls": "📞 Mis llamadas",
    "profile": "👤 Mi perfil",

    "model_title": "🔥💋 MODO MODELO 💋🔥",

    "model_profile": "👤 Mi perfil",
    "content": "📸 Mi contenido",
    "publish": "➕ Publicar contenido",
    "earnings": "💰 Mis ganancias",
    "sales": "📊 Mis ventas",
    "model_calls": "📞 Mis llamadas",
    "my_agency": "🏢 Mi agencia",
    "withdraw": "💸 Solicitar retiro",
    "model_channel": "📢 Canal exclusivo de Musas",

    "agency_title": "🏢🔥 MODO AGENCIA 🔥🏢",

    "models": "👩‍👩‍👧 Mis Musas",
    "recruit": "➕ Reclutar Musa",
    "codes": "🔑 Mis códigos",
    "team_sales": "📊 Ventas del equipo",
    "commissions": "💰 Mis comisiones",
    "agency_withdraw": "💸 Solicitar retiro",
    "agency_profile": "📝 Mi agencia",
    "create_agency": "🏗️ Crear agencia",
    "agency_channel": "📢 Canal exclusivo de Agencias",

    "back": "⬅️ Volver",

    "balance_text": (
        "⭐💎 MI SALDO 💎⭐\n\n"
        "💎 Saldo disponible: 0 puntos\n\n"
        "🔥 Próximamente podrás recargar tu saldo."
    ),

    "history_text": (
        "📜💎 HISTORIAL 💎📜\n\n"
        "Aquí aparecerán tus recargas, "
        "contenido desbloqueado y llamadas."
    ),

    "coming": (
        "🚀🔥 PRÓXIMAMENTE 🔥\n\n"
        "Estamos preparando esta función "
        "para Velvet Musa. 🖤😈"
    )
}


# =========================================================
# TEXTOS INGLÉS
# =========================================================

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
        "📸 Discover exclusive content\n"
        "📞 Spend some private time together 🔥\n\n"
        "😈 You might find exactly what you've been looking for…\n\n"
        "👇 Choose an option:"
    ),

    "user_title": "👤💎 USER MODE 💎👤",

    "explore": "🔎 Explore Muses",
    "balance": "⭐ My balance",
    "recharge": "💰 Add balance",
    "history": "📜 History",
    "calls": "📞 My calls",
    "profile": "👤 My profile",

    "model_title": "🔥💋 MODEL MODE 💋🔥",

    "model_profile": "👤 My profile",
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

    "back": "⬅️ Back",

    "balance_text": (
        "⭐💎 MY BALANCE 💎⭐\n\n"
        "💎 Available balance: 0 points\n\n"
        "🔥 Balance top-ups will be available soon."
    ),

    "history_text": (
        "📜💎 HISTORY 💎📜\n\n"
        "Your top-ups, unlocked content "
        "and calls will appear here."
    ),

    "coming": (
        "🚀🔥 COMING SOON 🔥\n\n"
        "We're preparing this feature "
        "for Velvet Musa. 🖤😈"
    )
}


# =========================================================
# IDIOMA
# =========================================================

def get_texts(context):
    if context.user_data.get("language") == "en":
        return EN

    return ES


# =========================================================
# MENÚ INFERIOR
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
# MENÚ USUARIO
# =========================================================

def user_menu(t):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                t["explore"],
                callback_data="explore"
            )
        ],
        [
            InlineKeyboardButton(
                t["balance"],
                callback_data="balance"
            )
        ],
        [
            InlineKeyboardButton(
                t["recharge"],
                callback_data="recharge"
            )
        ],
        [
            InlineKeyboardButton(
                t["history"],
                callback_data="history"
            )
        ],
        [
            InlineKeyboardButton(
                t["calls"],
                callback_data="user_calls"
            )
        ],
        [
            InlineKeyboardButton(
                t["profile"],
                callback_data="user_profile"
            )
        ],
        [
            InlineKeyboardButton(
                t["back"],
                callback_data="home"
            )
        ]
    ])


# =========================================================
# MENÚ MODELO
# =========================================================

def model_menu(t):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                t["model_profile"],
                callback_data="model_profile"
            )
        ],
        [
            InlineKeyboardButton(
                t["content"],
                callback_data="model_content"
            )
        ],
        [
            InlineKeyboardButton(
                t["publish"],
                callback_data="publish"
            )
        ],
        [
            InlineKeyboardButton(
                t["earnings"],
                callback_data="earnings"
            )
        ],
        [
            InlineKeyboardButton(
                t["sales"],
                callback_data="sales"
            )
        ],
        [
            InlineKeyboardButton(
                t["model_calls"],
                callback_data="model_calls"
            )
        ],
        [
            InlineKeyboardButton(
                t["my_agency"],
                callback_data="my_agency"
            )
        ],
        [
            InlineKeyboardButton(
                t["withdraw"],
                callback_data="withdraw"
            )
        ],
        [
            InlineKeyboardButton(
                t["model_channel"],
                url=MODELS_CHANNEL
            )
        ],
        [
            InlineKeyboardButton(
                t["back"],
                callback_data="home"
            )
        ]
    ])


# =========================================================
# MENÚ AGENCIA
# =========================================================

def agency_menu(t):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                t["models"],
                callback_data="models"
            )
        ],
        [
            InlineKeyboardButton(
                t["recruit"],
                callback_data="recruit"
            )
        ],
        [
            InlineKeyboardButton(
                t["codes"],
                callback_data="codes"
            )
        ],
        [
            InlineKeyboardButton(
                t["team_sales"],
                callback_data="team_sales"
            )
        ],
        [
            InlineKeyboardButton(
                t["commissions"],
                callback_data="commissions"
            )
        ],
        [
            InlineKeyboardButton(
                t["agency_withdraw"],
                callback_data="agency_withdraw"
            )
        ],
        [
            InlineKeyboardButton(
                t["agency_profile"],
                callback_data="agency_profile"
            )
        ],
        [
            InlineKeyboardButton(
                t["create_agency"],
                callback_data="create_agency"
            )
        ],
        [
            InlineKeyboardButton(
                t["agency_channel"],
                url=AGENCY_CHANNEL
            )
        ],
        [
            InlineKeyboardButton(
                t["back"],
                callback_data="home"
            )
        ]
    ])


# =========================================================
# REGISTRO DE MUSA
# =========================================================

def registration_start():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "❌ Cancelar",
                callback_data="cancel_registration"
            )
        ]
    ])


async def start_model_registration(
    update,
    context
):
    query = update.callback_query

    context.user_data["registration"] = {
        "step": "artistic_name"
    }

    await query.edit_message_text(
        "🔥💋 REGISTRO DE MUSA 💋🔥\n\n"
        "Vamos a crear tu identidad dentro de "
        "Velvet Musa.\n\n"
        "👩 Primero:\n\n"
        "Escribe el **nombre artístico** con el "
        "que quieres que te conozcan.\n\n"
        "Ejemplo: Melissa",
        parse_mode="Markdown",
        reply_markup=registration_start()
    )


async def process_registration_message(
    update,
    context
):
    registration = context.user_data.get("registration")

    if not registration:
        return False

    step = registration.get("step")
    message = update.message

    if step == "artistic_name":
        if not message.text:
            await message.reply_text(
                "❌ Escribe tu nombre artístico en texto."
            )
            return True

        name = message.text.strip()

        if len(name) < 2 or len(name) > 30:
            await message.reply_text(
                "❌ El nombre debe tener entre "
                "2 y 30 caracteres."
            )
            return True

        registration["artistic_name"] = name
        registration["step"] = "velvet_username"

        await message.reply_text(
            "✨ Perfecto.\n\n"
            "Ahora elige tu **@usuario de Velvet Musa**.\n\n"
            "🔐 Este NO tiene que ser tu usuario de "
            "Telegram.\n\n"
            "Ejemplo:\n"
            "@Melissa35\n\n"
            "Este será el nombre que verán los usuarios.",
            parse_mode="Markdown"
        )

        return True

    if step == "velvet_username":
        if not message.text:
            await message.reply_text(
                "❌ Escribe un @usuario."
            )
            return True

        username = message.text.strip().replace("@", "")

        if not username.replace("_", "").isalnum():
            await message.reply_text(
                "❌ El usuario solo puede contener "
                "letras, números y _."
            )
            return True

        if len(username) < 3 or len(username) > 24:
            await message.reply_text(
                "❌ El usuario debe tener entre "
                "3 y 24 caracteres."
            )
            return True

        telegram_id = update.effective_user.id

        if not username_available(
            username,
            telegram_id
        ):
            await message.reply_text(
                "❌ Ese @usuario ya está ocupado.\n\n"
                "Prueba con otro."
            )
            return True

        registration["velvet_username"] = username
        registration["step"] = "photo"

        await message.reply_text(
            "📸 Ahora envíame tu **foto principal**.\n\n"
            "Esta será la foto que aparecerá como "
            "miniatura de tu perfil.\n\n"
            "✨ Elige una foto bonita y clara."
        )

        return True

    if step == "photo":
        if not message.photo:
            await message.reply_text(
                "📸 Necesito que me envíes una foto.\n\n"
                "Pulsa el clip 📎 y selecciona una imagen."
            )
            return True

        photo = message.photo[-1]

        registration["photo_file_id"] = photo.file_id
        registration["step"] = "description"

        await message.reply_text(
            "😍 ¡Foto recibida!\n\n"
            "Ahora escribe una **descripción corta** "
            "para tu perfil.\n\n"
            "Ejemplo:\n"
            "«Soy Melissa, divertida, conversadora "
            "y me encanta conocer personas nuevas. 😈»"
        )

        return True

    if step == "description":
        if not message.text:
            await message.reply_text(
                "❌ Escribe una descripción para continuar."
            )
            return True

        description = message.text.strip()

        if len(description) < 5 or len(description) > 500:
            await message.reply_text(
                "❌ La descripción debe tener entre "
                "5 y 500 caracteres."
            )
            return True

        registration["description"] = description
        registration["step"] = "services"

        await message.reply_text(
            "🔥 Ahora vamos a elegir tus servicios.\n\n"
            "Puedes ofrecer uno, varios o todos.\n\n"
            "👇 Pulsa los servicios que quieras activar:",
            reply_markup=services_keyboard(registration)
        )

        return True

    return False


def services_keyboard(data):
    def mark(enabled):
        return "✅" if enabled else "⬜"

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                f"{mark(data.get('chat_enabled', False))} 💬 Chat",
                callback_data="reg_toggle_chat"
            )
        ],
        [
            InlineKeyboardButton(
                f"{mark(data.get('photos_enabled', False))} 📸 Fotos",
                callback_data="reg_toggle_photos"
            )
        ],
        [
            InlineKeyboardButton(
                f"{mark(data.get('videos_enabled', False))} 🎥 Vídeos",
                callback_data="reg_toggle_videos"
            )
        ],
        [
            InlineKeyboardButton(
                f"{mark(data.get('calls_enabled', False))} 📞 Llamadas",
                callback_data="reg_toggle_calls"
            )
        ],
        [
            InlineKeyboardButton(
                "💎 Continuar",
                callback_data="reg_prices"
            )
        ],
        [
            InlineKeyboardButton(
                "❌ Cancelar",
                callback_data="cancel_registration"
            )
        ]
    ])


async def registration_callback(
    update,
    context
):
    query = update.callback_query
    await query.answer()

    registration = context.user_data.get("registration")

    if not registration:
        await query.edit_message_text(
            "❌ No hay un registro activo."
        )
        return

    data = query.data

    if data == "cancel_registration":
        context.user_data.pop("registration", None)

        t = get_texts(context)

        await query.edit_message_text(
            t["model_title"],
            reply_markup=model_menu(t)
        )
        return

    if data == "reg_toggle_chat":
        registration["chat_enabled"] = not registration.get(
            "chat_enabled",
            False
        )

        await query.edit_message_reply_markup(
            reply_markup=services_keyboard(registration)
        )
        return

    if data == "reg_toggle_photos":
        registration["photos_enabled"] = not registration.get(
            "photos_enabled",
            False
        )

        await query.edit_message_reply_markup(
            reply_markup=services_keyboard(registration)
        )
        return

    if data == "reg_toggle_videos":
        registration["videos_enabled"] = not registration.get(
            "videos_enabled",
            False
        )

        await query.edit_message_reply_markup(
            reply_markup=services_keyboard(registration)
        )
        return

    if data == "reg_toggle_calls":
        registration["calls_enabled"] = not registration.get(
            "calls_enabled",
            False
        )

        await query.edit_message_reply_markup(
            reply_markup=services_keyboard(registration)
        )
        return

    if data == "reg_prices":
        if not any([
            registration.get("chat_enabled", False),
            registration.get("photos_enabled", False),
            registration.get("videos_enabled", False),
            registration.get("calls_enabled", False)
        ]):
            await query.answer(
                "Activa al menos un servicio.",
                show_alert=True
            )
            return

        registration["step"] = "prices"

        await query.edit_message_text(
            "💎 Ahora configuraremos tus precios.\n\n"
            "Primero escribe el precio del **Chat**.\n\n"
            "Si no activaste Chat, escribe:\n"
            "0",
            parse_mode="Markdown"
        )


async def process_price_message(
    update,
    context
):
    registration = context.user_data.get("registration")

    if not registration:
        return False

    if registration.get("step") != "prices":
        return False

    if not update.message.text:
        return True

    text = update.message.text.strip()

    try:
        price = int(text)
    except ValueError:
        await update.message.reply_text(
            "❌ Escribe solamente un número.\n\n"
            "Ejemplo: 1"
        )
        return True

    if price < 0 or price > 100000:
        await update.message.reply_text(
            "❌ El precio debe estar entre 0 y 100000 puntos."
        )
        return True

    current = registration.get("price_step", "chat")

    if current == "chat":
        registration["chat_price"] = price
        registration["price_step"] = "photos"

        await update.message.reply_text(
            "📸 Precio de las **fotos**.\n\n"
            "Si no activaste Fotos, escribe 0.",
            parse_mode="Markdown"
        )

        return True

    if current == "photos":
        registration["photos_price"] = price
        registration["price_step"] = "videos"

        await update.message.reply_text(
            "🎥 Precio de los **vídeos**.\n\n"
            "Si no activaste Vídeos, escribe 0.",
            parse_mode="Markdown"
        )

        return True

    if current == "videos":
        registration["videos_price"] = price
        registration["price_step"] = "calls"

        await update.message.reply_text(
            "📞 Precio de las **llamadas por minuto**.\n\n"
            "Si no activaste Llamadas, escribe 0.",
            parse_mode="Markdown"
        )

        return True

    if current == "calls":
        registration["calls_price"] = price

        telegram_id = update.effective_user.id

        save_model(
            telegram_id,
            registration
        )

        context.user_data.pop("registration", None)

        await update.message.reply_text(
            "🎉🔥 ¡REGISTRO COMPLETADO! 🔥🎉\n\n"
            f"👩 {registration['artistic_name']}\n"
            f"🔤 @{registration['velvet_username']}\n\n"
            "📝 Tu perfil ha sido creado.\n\n"
            "🔐 Tu Telegram personal permanecerá "
            "oculto para los usuarios.\n\n"
            "🖤 Bienvenida a Velvet Musa.",
            reply_markup=model_menu(get_texts(context))
        )

        return True

    return False


# =========================================================
# INICIO
# =========================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
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


# =========================================================
# MENÚ DE TEXTO
# =========================================================

async def text_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if context.user_data.get("registration"):
        if await process_registration_message(
            update,
            context
        ):
            return

        if await process_price_message(
            update,
            context
        ):
            return

    t = get_texts(context)
    text = update.message.text

    if text == t["home"]:
        await start(update, context)
        return

    if text == t["user"]:
        await update.message.reply_text(
            t["user_title"],
            reply_markup=user_menu(t)
        )
        return

    if text == t["model"]:
        await update.message.reply_text(
            t["model_title"],
            reply_markup=model_menu(t)
        )
        return

    if text == t["agency"]:
        await update.message.reply_text(
            t["agency_title"],
            reply_markup=agency_menu(t)
        )
        return

    if text == t["language"]:
        if context.user_data.get("language") == "en":
            context.user_data["language"] = "es"
        else:
            context.user_data["language"] = "en"

        t = get_texts(context)

        await update.message.reply_text(
            "🌎 " + t["language"] + " ✅",
            reply_markup=bottom_menu(t)
        )


# =========================================================
# MELISSA DE PRUEBA
# =========================================================

async def show_melissa(
    update,
    context
):
    query = update.callback_query
    t = get_texts(context)

    menu = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "💋 Ver perfil",
                callback_data="melissa_profile"
            )
        ],
        [
            InlineKeyboardButton(
                "➡️ Siguiente Musa",
                callback_data="next_muse"
            )
        ],
        [
            InlineKeyboardButton(
                t["back"],
                callback_data="user"
            )
        ]
    ])

    caption = (
        "🔥💋 DESCUBRE NUESTRAS MUSAS 💋🔥\n\n"
        "👩 Melissa · 35 años · 🇨🇴 Colombia\n\n"
        "✨ Divertida, conversadora y lista para "
        "compartir momentos especiales. 😈\n\n"
        "🟢 Disponible\n"
        "💬 Chat: 1 💎/mensaje\n"
        "📸 Fotos: 20 💎\n"
        "🎥 Vídeos: 50 💎\n"
        "📞 Llamada: 25 💎/min"
    )

    try:
        await query.message.reply_photo(
            photo=MELISSA_PHOTO_URL,
            caption=caption,
            reply_markup=menu
        )

        await query.answer()

    except Exception:
        await query.edit_message_text(
            caption,
            reply_markup=menu
        )


# =========================================================
# PERFIL DE MUSA
# =========================================================

def model_profile_keyboard(
    model,
    back_callback="explore"
):
    buttons = []

    if model["chat_enabled"]:
        buttons.append([
            InlineKeyboardButton(
                f"💬 Chatear · {model['chat_price']} 💎/mensaje",
                callback_data=f"chat_{model['id']}"
            )
        ])

    if model["photos_enabled"]:
        buttons.append([
            InlineKeyboardButton(
                f"📸 Fotos · {model['photos_price']} 💎",
                callback_data=f"photos_{model['id']}"
            )
        ])

    if model["videos_enabled"]:
        buttons.append([
            InlineKeyboardButton(
                f"🎥 Vídeos · {model['videos_price']} 💎",
                callback_data=f"videos_{model['id']}"
            )
        ])

    if model["calls_enabled"]:
        buttons.append([
            InlineKeyboardButton(
                f"📞 Llamada · {model['calls_price']} 💎/min",
                callback_data=f"call_{model['id']}"
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            "⬅️ Volver",
            callback_data=back_callback
        )
    ])

    return InlineKeyboardMarkup(buttons)


async def show_model_profile(
    update,
    context,
    model
):
    query = update.callback_query

    text = (
        f"👩🔥 {model['artistic_name'].upper()} 🔥👩\n\n"
        f"🔤 @{model['velvet_username']}\n\n"
        f"📝 {model['description']}\n\n"
        "✨ Elige cómo quieres conocerla:"
    )

    await query.edit_message_text(
        text,
        reply_markup=model_profile_keyboard(model)
    )


# =========================================================
# BOTONES
# =========================================================

async def buttons(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    t = get_texts(context)
    data = query.data

    # -----------------------------------------------------
    # MENÚS PRINCIPALES
    # -----------------------------------------------------

    if data == "home":
        await query.edit_message_text(
            t["welcome"]
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

    # -----------------------------------------------------
    # REGISTRO DE MUSA
    # -----------------------------------------------------

    if data == "start_model_registration":
        await start_model_registration(
            update,
            context
        )
        return

    if data.startswith("reg_"):
        await registration_callback(
            update,
            context
        )
        return

    if data == "cancel_registration":
        context.user_data.pop("registration", None)

        await query.edit_message_text(
            t["model_title"],
            reply_markup=model_menu(t)
        )
        return

    # -----------------------------------------------------
    # EXPLORAR
    # -----------------------------------------------------

    if data == "explore":
        await show_melissa(
            update,
            context
        )
        return

    # -----------------------------------------------------
    # PERFIL MELISSA
    # -----------------------------------------------------

    if data == "melissa_profile":
        await query.edit_message_text(
            "👩🔥 MELISSA · 35 AÑOS 🔥👩\n\n"
            "🔤 @Melissa35\n"
            "🇨🇴 Colombia\n\n"
            "✨ Divertida, conversadora y lista para "
            "compartir momentos especiales. 😈\n\n"
            "🟢 Disponible\n\n"
            "💬 Chat — 1 💎/mensaje\n"
            "📸 Fotos — 20 💎\n"
            "🎥 Vídeos — 50 💎\n"
            "📞 Llamada — 25 💎/min\n\n"
            "🔐 Cada servicio se cobra por separado.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "💬 Chatear · 1 💎/mensaje",
                        callback_data="melissa_chat"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📸 Fotos · 20 💎",
                        callback_data="melissa_photos"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🎥 Vídeos · 50 💎",
                        callback_data="melissa_videos"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📞 Llamada · 25 💎/min",
                        callback_data="melissa_call"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "⬅️ Volver",
                        callback_data="explore"
                    )
                ]
            ])
        )
        return

    # -----------------------------------------------------
    # MELISSA - CHAT
    # -----------------------------------------------------

    if data == "melissa_chat":
        await query.edit_message_text(
            "💬🔥 CHAT CON MELISSA 🔥💬\n\n"
            "👩 Melissa · @Melissa35\n\n"
            "💎 Precio: 1 punto por mensaje.\n\n"
            "😈 El sistema de chat intermediado "
            "estará disponible en la siguiente etapa.\n\n"
            "🔐 Melissa nunca verá tu número "
            "ni tu usuario personal de Telegram.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "⬅️ Volver",
                        callback_data="melissa_profile"
                    )
                ]
            ])
        )
        return

    # -----------------------------------------------------
    # MELISSA - FOTOS
    # -----------------------------------------------------

    if data == "melissa_photos":
        await query.edit_message_text(
            "📸🔒 FOTOS EXCLUSIVAS 🔒📸\n\n"
            "💎 Precio: 20 puntos.\n\n"
            "El contenido privado no aparecerá "
            "en el perfil público.\n\n"
            "🔐 Cuando conectemos el sistema de pagos, "
            "la foto se entregará como contenido protegido.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "⬅️ Volver",
                        callback_data="melissa_profile"
                    )
                ]
            ])
        )
        return

    # -----------------------------------------------------
    # MELISSA - VÍDEOS
    # -----------------------------------------------------

    if data == "melissa_videos":
        await query.edit_message_text(
            "🎥🔒 VÍDEOS EXCLUSIVOS 🔒🎥\n\n"
            "💎 Precio: 50 puntos.\n\n"
            "Los vídeos privados no aparecerán "
            "en el perfil público.\n\n"
            "🔐 Cuando conectemos el sistema de pagos, "
            "se enviarán como contenido protegido.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "⬅️ Volver",
                        callback_data="melissa_profile"
                    )
                ]
            ])
        )
        return

    # -----------------------------------------------------
    # MELISSA - LLAMADA
    # -----------------------------------------------------

    if data == "melissa_call":
        await query.edit_message_text(
            "📞🔥 LLAMADA PRIVADA 🔥📞\n\n"
            "👩 Melissa · @Melissa35\n"
            "💎 25 puntos por minuto.\n\n"
            "🔐 El número personal de Melissa "
            "nunca será mostrado al usuario.\n\n"
            "La comunicación se realizará mediante "
            "Velvet Musa cuando activemos el sistema.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "⬅️ Volver",
                        callback_data="melissa_profile"
                    )
                ]
            ])
        )
        return

    # -----------------------------------------------------
    # SIGUIENTE MUSA
    # -----------------------------------------------------

    if data == "next_muse":
        models = get_all_models()

        if models:
            await query.edit_message_text(
                "👩🔥 MUSAS REGISTRADAS 🔥👩\n\n"
                f"Actualmente tenemos {len(models)} "
                "Musa(s) registrada(s).\n\n"
                "✨ Pronto mostraremos sus perfiles "
                "individualmente.",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton(
                            "⬅️ Volver",
                            callback_data="explore"
                        )
                    ]
                ])
            )
        else:
            await query.edit_message_text(
                "✨🔥 PRÓXIMAMENTE 🔥✨\n\n"
                "Estamos preparando más Musas para "
                "Velvet Musa. 😈",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton(
                            "⬅️ Volver",
                            callback_data="explore"
                        )
                    ]
                ])
            )

        return

    # -----------------------------------------------------
    # SALDO
    # -----------------------------------------------------

    if data == "balance":
        await query.edit_message_text(
            t["balance_text"],
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        t["recharge"],
                        callback_data="recharge"
                    )
                ],
                [
                    InlineKeyboardButton(
                        t["back"],
                        callback_data="user"
                    )
                ]
            ])
        )
        return

    # -----------------------------------------------------
    # RECARGAR
    # -----------------------------------------------------

    if data == "recharge":
        await query.edit_message_text(
            t["coming"],
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        t["back"],
                        callback_data="user"
                    )
                ]
            ])
        )
        return

    # -----------------------------------------------------
    # HISTORIAL
    # -----------------------------------------------------

    if data == "history":
        await query.edit_message_text(
            t["history_text"],
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        t["back"],
                        callback_data="user"
                    )
                ]
            ])
        )
        return

    # -----------------------------------------------------
    # PERFIL / LLAMADAS USUARIO
    # -----------------------------------------------------

    if data in [
        "user_calls",
        "user_profile"
    ]:
        await query.edit_message_text(
            t["coming"],
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        t["back"],
                        callback_data="user"
                    )
                ]
            ])
        )
        return

    # -----------------------------------------------------
    # PERFIL MODELO ACTUAL
    # -----------------------------------------------------

    if data == "model_profile":
        telegram_id = update.effective_user.id

        model = get_model_by_telegram_id(
            telegram_id
        )

        if model is None:
            await query.edit_message_text(
                "👩🔥 MI PERFIL 🔥👩\n\n"
                "Todavía no tienes un perfil creado.\n\n"
                "💋 Pulsa el botón para registrarte.",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton(
                            "🔥 Crear mi perfil",
                            callback_data="start_model_registration"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "⬅️ Volver",
                            callback_data="model"
                        )
                    ]
                ])
            )
            return

        await show_registered_model(
            query,
            model
        )
        return

    # -----------------------------------------------------
    # ACCIONES MODELO
    # -----------------------------------------------------

    model_actions = [
        "model_content",
        "publish",
        "earnings",
        "sales",
        "model_calls",
        "my_agency",
        "withdraw"
    ]

    if data in model_actions:
        await query.edit_message_text(
            t["coming"],
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        t["back"],
                        callback_data="model"
                    )
                ]
            ])
        )
        return

    # -----------------------------------------------------
    # ACCIONES AGENCIA
    # -----------------------------------------------------

    agency_actions = [
        "models",
        "recruit",
        "codes",
        "team_sales",
        "commissions",
        "agency_withdraw",
        "agency_profile",
        "create_agency"
    ]

    if data in agency_actions:
        await query.edit_message_text(
            t["coming"],
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        t["back"],
                        callback_data="agency"
                    )
                ]
            ])
        )
        return

    # -----------------------------------------------------
    # ACCIONES DE UNA MUSA REGISTRADA
    # -----------------------------------------------------

    if data.startswith("chat_"):
        model_id = int(data.split("_")[1])

        await query.edit_message_text(
            "💬🔥 CHAT 🔥💬\n\n"
            "El sistema de chat intermediado "
            "se conectará en la siguiente etapa.\n\n"
            "🔐 La identidad personal de la Musa "
            "permanecerá protegida.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "⬅️ Volver",
                        callback_data=f"profile_{model_id}"
                    )
                ]
            ])
        )
        return

    if data.startswith("photos_"):
        model_id = int(data.split("_")[1])

        await query.edit_message_text(
            "📸🔒 FOTOS EXCLUSIVAS 🔒📸\n\n"
            "El sistema de compra de contenido "
            "se conectará en la siguiente etapa.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "⬅️ Volver",
                        callback_data=f"profile_{model_id}"
                    )
                ]
            ])
        )
        return

    if data.startswith("videos_"):
        model_id = int(data.split("_")[1])

        await query.edit_message_text(
            "🎥🔒 VÍDEOS EXCLUSIVOS 🔒🎥\n\n"
            "El sistema de compra de contenido "
            "se conectará en la siguiente etapa.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "⬅️ Volver",
                        callback_data=f"profile_{model_id}"
                    )
                ]
            ])
        )
        return

    if data.startswith("call_"):
        model_id = int(data.split("_")[1])

        await query.edit_message_text(
            "📞🔥 LLAMADA PRIVADA 🔥📞\n\n"
            "El sistema de llamadas intermediadas "
            "se conectará en la siguiente etapa.\n\n"
            "🔐 Ningún número personal será mostrado.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "⬅️ Volver",
                        callback_data=f"profile_{model_id}"
                    )
                ]
            ])
        )
        return

    if data.startswith("profile_"):
        model_id = int(data.split("_")[1])

        connection = db_connect()

        model = connection.execute(
            """
            SELECT *
            FROM models
            WHERE id = ?
            """,
            (model_id,)
        ).fetchone()

        connection.close()

        if model is None:
            await query.edit_message_text(
                "❌ Esta Musa ya no está disponible.",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton(
                            "⬅️ Volver",
                            callback_data="explore"
                        )
                    ]
                ])
            )
            return

        await show_registered_model(
            query,
            model
        )
        return


# =========================================================
# MOSTRAR PERFIL REGISTRADO
# =========================================================

async def show_registered_model(
    query,
    model
):
    text = (
        f"👩🔥 {model['artistic_name'].upper()} 🔥👩\n\n"
        f"🔤 @{model['velvet_username']}\n\n"
        f"📝 {model['description']}\n\n"
        "✨ Servicios disponibles:"
    )

    await query.edit_message_text(
        text,
        reply_markup=model_profile_keyboard(
            model,
            back_callback="model"
        )
    )


# =========================================================
# MENSAJES DE FOTOS Y TEXTO
# =========================================================

async def message_router(
    update,
    context
):
    if context.user_data.get("registration"):
        registration = context.user_data["registration"]

        if registration.get("step") == "photo":
            handled = await process_registration_message(
                update,
                context
            )

            if handled:
                return

        if registration.get("step") in [
            "artistic_name",
            "velvet_username",
            "description"
        ]:
            handled = await process_registration_message(
                update,
                context
            )

            if handled:
                return

        if registration.get("step") == "prices":
            handled = await process_price_message(
                update,
                context
            )

            if handled:
                return

    await text_menu(
        update,
        context
    )


# =========================================================
# MAIN
# =========================================================

def main():
    init_database()

    Thread(
        target=run_web,
        daemon=True
    ).start()

    application = (
        Application
        .builder()
        .token(TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            buttons
        )
    )

    application.add_handler(
        MessageHandler(
            filters.PHOTO,
            message_router
        )
    )

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            message_router
        )
    )

    print(
        "🌟 Velvet Musa: bot iniciado correctamente 🔥"
    )

    application.run_polling()


if __name__ == "__main__":
    main()
