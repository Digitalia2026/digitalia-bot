import os
import json
import hashlib
import secrets
from threading import Thread

from flask import Flask
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)


# =========================================================
# CONFIGURACIÓN
# =========================================================

TOKEN = os.getenv("BOT_TOKEN")

MELISSA_PHOTO_URL = (
    "https://i.ibb.co/VYpN8wtP/"
    "Chat-GPT-Image-1-ago-2026-06-35-15-p-m.png"
)

MODELS_CHANNEL = "https://t.me/+BUxwqByLYK00ZTYx"
AGENCY_CHANNEL = "https://t.me/+MrTIOV4GlqAzNWIx"

DATA_FILE = "velvet_data.json"


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
        port=port,
    )


# =========================================================
# BASE DE DATOS SIMPLE JSON
# =========================================================

def load_data():
    if not os.path.exists(DATA_FILE):
        return {
            "models": {},
            "users": {},
        }

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if "models" not in data:
            data["models"] = {}

        if "users" not in data:
            data["users"] = {}

        return data

    except Exception:
        return {
            "models": {},
            "users": {},
        }


def save_data(data):
    temp_file = DATA_FILE + ".tmp"

    with open(
        temp_file,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2,
        )

    os.replace(
        temp_file,
        DATA_FILE,
    )


DATA = load_data()


# =========================================================
# SEGURIDAD DEL PIN
# =========================================================

def hash_pin(pin):
    salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        pin.encode("utf-8"),
        salt.encode("utf-8"),
        120000,
    ).hex()

    return f"{salt}${password_hash}"


def verify_pin(pin, stored_hash):
    try:
        salt, password_hash = stored_hash.split("$", 1)

        calculated_hash = hashlib.pbkdf2_hmac(
            "sha256",
            pin.encode("utf-8"),
            salt.encode("utf-8"),
            120000,
        ).hex()

        return secrets.compare_digest(
            calculated_hash,
            password_hash,
        )

    except Exception:
        return False


# =========================================================
# TEXTOS
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
        "🚀🔥 PRÓXIMAMENTE 🔥🔥\n\n"
        "Estamos preparando esta función "
        "para Velvet Musa. 🖤😈"
    ),
}


def get_texts(context):
    return ES


# =========================================================
# MENÚ INFERIOR
# =========================================================

def bottom_menu(t):
    return ReplyKeyboardMarkup(
        [
            [t["home"], t["user"]],
            [t["model"], t["agency"]],
            [t["language"]],
        ],
        resize_keyboard=True,
        is_persistent=True,
    )


# =========================================================
# MENÚ USUARIO
# =========================================================

def user_menu(t):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                t["explore"],
                callback_data="explore",
            )
        ],
        [
            InlineKeyboardButton(
                t["balance"],
                callback_data="balance",
            )
        ],
        [
            InlineKeyboardButton(
                t["recharge"],
                callback_data="recharge",
            )
        ],
        [
            InlineKeyboardButton(
                t["history"],
                callback_data="history",
            )
        ],
        [
            InlineKeyboardButton(
                t["calls"],
                callback_data="user_calls",
            )
        ],
        [
            InlineKeyboardButton(
                t["profile"],
                callback_data="user_profile",
            )
        ],
        [
            InlineKeyboardButton(
                t["back"],
                callback_data="home",
            )
        ],
    ])


# =========================================================
# MENÚ MODELO
# =========================================================

def model_menu(t):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                t["model_profile"],
                callback_data="model_profile",
            )
        ],
        [
            InlineKeyboardButton(
                t["content"],
                callback_data="model_content",
            )
        ],
        [
            InlineKeyboardButton(
                t["publish"],
                callback_data="publish",
            )
        ],
        [
            InlineKeyboardButton(
                t["earnings"],
                callback_data="earnings",
            )
        ],
        [
            InlineKeyboardButton(
                t["sales"],
                callback_data="sales",
            )
        ],
        [
            InlineKeyboardButton(
                t["model_calls"],
                callback_data="model_calls",
            )
        ],
        [
            InlineKeyboardButton(
                t["my_agency"],
                callback_data="my_agency",
            )
        ],
        [
            InlineKeyboardButton(
                t["withdraw"],
                callback_data="withdraw",
            )
        ],
        [
            InlineKeyboardButton(
                t["model_channel"],
                url=MODELS_CHANNEL,
            )
        ],
        [
            InlineKeyboardButton(
                t["back"],
                callback_data="home",
            )
        ],
    ])


# =========================================================
# MENÚ AGENCIA
# =========================================================

def agency_menu(t):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                t["models"],
                callback_data="models",
            )
        ],
        [
            InlineKeyboardButton(
                t["recruit"],
                callback_data="recruit",
            )
        ],
        [
            InlineKeyboardButton(
                t["codes"],
                callback_data="codes",
            )
        ],
        [
            InlineKeyboardButton(
                t["team_sales"],
                callback_data="team_sales",
            )
        ],
        [
            InlineKeyboardButton(
                t["commissions"],
                callback_data="commissions",
            )
        ],
        [
            InlineKeyboardButton(
                t["agency_withdraw"],
                callback_data="agency_withdraw",
            )
        ],
        [
            InlineKeyboardButton(
                t["agency_profile"],
                callback_data="agency_profile",
            )
        ],
        [
            InlineKeyboardButton(
                t["create_agency"],
                callback_data="create_agency",
            )
        ],
        [
            InlineKeyboardButton(
                t["agency_channel"],
                url=AGENCY_CHANNEL,
            )
        ],
        [
            InlineKeyboardButton(
                t["back"],
                callback_data="home",
            )
        ],
    ])


# =========================================================
# REGISTRO DE MUSA
# =========================================================

def registration_cancel_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "❌ Cancelar registro",
                callback_data="cancel_registration",
            )
        ]
    ])


async def begin_model_access(update, context):
    user_id = str(update.effective_user.id)

    model = DATA["models"].get(user_id)

    if model:
        context.user_data["model_authenticated"] = False
        context.user_data["model_login"] = True

        await update.message.reply_text(
            "🔐💋 ACCESO DE MUSA 💋🔐\n\n"
            f"Hola, {model['public_name']} 🖤\n\n"
            "Introduce tu PIN para entrar a tu panel.\n\n"
            "🔢 El PIN debe ser el que elegiste "
            "durante tu registro."
        )

        return

    await update.message.reply_text(
        "🔥💋 ACCESO DE MUSAS 💋🔥\n\n"
        "No encontramos una cuenta de Musa asociada "
        "a este Telegram.\n\n"
        "Puedes registrarte gratis y crear tu perfil "
        "dentro de Velvet Musa. 🖤",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "✨ Registrarme como Musa",
                    callback_data="register_model",
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Volver",
                    callback_data="home",
                )
            ],
        ]),
    )


async def start_registration(update, context):
    query = update.callback_query

    await query.answer()

    context.user_data["registration"] = {
        "step": "name",
    }

    await query.edit_message_text(
        "✨💋 REGISTRO DE MUSA 💋✨\n\n"
        "Paso 1 de 5\n\n"
        "👩 Escribe el **nombre público** que quieres "
        "usar en Velvet Musa.\n\n"
        "💡 Este nombre será el que verán los usuarios.\n"
        "Tu nombre real de Telegram no se mostrará.",
        parse_mode="Markdown",
        reply_markup=registration_cancel_keyboard(),
    )


# =========================================================
# FINALIZAR REGISTRO
# =========================================================

async def finish_registration(update, context):
    user_id = str(update.effective_user.id)
    registration = context.user_data.get("registration")

    if not registration:
        return

    public_name = registration["name"]
    username = registration["username"]
    pin = registration["pin"]
    photo_file_id = registration.get("photo_file_id")

    username_key = username.lower()

    # Comprobar username
    for existing_model in DATA["models"].values():
        if existing_model.get("username", "").lower() == username_key:
            await update.message.reply_text(
                "❌ Ese nombre de usuario ya está ocupado.\n\n"
                "Escribe otro @usuario para Velvet Musa."
            )

            registration["step"] = "username"
            return

    DATA["models"][user_id] = {
        "public_name": public_name,
        "username": username,
        "age": registration.get("age", 18),
        "country": "🌎 Por configurar",
        "pin_hash": hash_pin(pin),
        "photo_file_id": photo_file_id,

        "chat": True,
        "photos": False,
        "videos": False,
        "calls": False,

        "chat_price": 2,
        "photo_price": 20,
        "video_price": 35,
        "call_price": 25,

        "balance": 0,
        "earnings": 0,
        "sales": 0,
    }

    save_data(DATA)

    context.user_data.pop("registration", None)
    context.user_data["model_authenticated"] = True
    context.user_data.pop("model_login", None)

    t = get_texts(context)

    await update.message.reply_text(
        "🎉🖤 ¡REGISTRO COMPLETADO! 🖤🎉\n\n"
        f"👩 Nombre público: {public_name}\n"
        f"🔖 Usuario: @{username}\n\n"
        "🔐 Tu cuenta está protegida por tu PIN.\n\n"
        "Ahora puedes configurar tus servicios "
        "desde tu panel de Musa.",
        reply_markup=bottom_menu(t),
    )

    await update.message.reply_text(
        t["model_title"],
        reply_markup=model_menu(t),
    )


# =========================================================
# PANEL DE MUSA
# =========================================================

def get_authenticated_model(update, context):
    user_id = str(update.effective_user.id)

    if not context.user_data.get("model_authenticated"):
        return None

    return DATA["models"].get(user_id)


def model_profile_text(model):
    chat = "✅ ACTIVADO" if model["chat"] else "🚫 DESACTIVADO"
    photos = "✅ ACTIVADAS" if model["photos"] else "🚫 DESACTIVADAS"
    videos = "✅ ACTIVADOS" if model["videos"] else "🚫 DESACTIVADOS"
    calls = "✅ ACTIVADAS" if model["calls"] else "🚫 DESACTIVADAS"

    return (
        "🔥💋 MI PERFIL DE MUSA 💋🔥\n\n"
        f"👩 Nombre público: {model['public_name']}\n"
        f"🔖 Usuario: @{model['username']}\n"
        f"🎂 Edad: {model['age']}\n"
        f"🌎 País: {model['country']}\n\n"
        "━━━━━━━━━━━━━━\n"
        "⚙️ SERVICIOS\n"
        "━━━━━━━━━━━━━━\n\n"
        f"💬 Chat: {chat}\n"
        f"   💎 {model['chat_price']} puntos por mensaje\n\n"
        f"📸 Fotos: {photos}\n"
        f"   💎 {model['photo_price']} puntos\n\n"
        f"🎥 Vídeos: {videos}\n"
        f"   💎 {model['video_price']} puntos\n\n"
        f"📞 Llamadas: {calls}\n"
        f"   💎 {model['call_price']} puntos/minuto\n\n"
        "Pulsa un servicio para activarlo o desactivarlo."
    )


def model_profile_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "💬 Activar/desactivar Chat",
                callback_data="toggle_chat",
            )
        ],
        [
            InlineKeyboardButton(
                "📸 Activar/desactivar Fotos",
                callback_data="toggle_photos",
            )
        ],
        [
            InlineKeyboardButton(
                "🎥 Activar/desactivar Vídeos",
                callback_data="toggle_videos",
            )
        ],
        [
            InlineKeyboardButton(
                "📞 Activar/desactivar Llamadas",
                callback_data="toggle_calls",
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ Volver",
                callback_data="model",
            )
        ],
    ])


# =========================================================
# PERFIL DE MELISSA PARA USUARIOS
# =========================================================

MELISSA_DEMO = {
    "public_name": "Melissa",
    "username": "Melissa35",
    "age": 35,
    "country": "🇨🇴 Colombia",
    "photo": MELISSA_PHOTO_URL,

    "chat": True,
    "photos": False,
    "videos": False,
    "calls": False,

    "chat_price": 2,
    "photo_price": 20,
    "video_price": 35,
    "call_price": 25,
}


def muse_profile_keyboard(muse):
    buttons = []

    if muse["chat"]:
        buttons.append([
            InlineKeyboardButton(
                f"✅ 💬 Chat — {muse['chat_price']} 💎/mensaje",
                callback_data="service_chat",
            )
        ])
    else:
        buttons.append([
            InlineKeyboardButton(
                "🚫 💬 Chat — No disponible",
                callback_data="inactive",
            )
        ])

    if muse["photos"]:
        buttons.append([
            InlineKeyboardButton(
                f"✅ 📸 Fotos — {muse['photo_price']} 💎",
                callback_data="service_photo",
            )
        ])
    else:
        buttons.append([
            InlineKeyboardButton(
                "🚫 📸 Fotos — No disponible",
                callback_data="inactive",
            )
        ])

    if muse["videos"]:
        buttons.append([
            InlineKeyboardButton(
                f"✅ 🎥 Vídeos — {muse['video_price']} 💎",
                callback_data="service_video",
            )
        ])
    else:
        buttons.append([
            InlineKeyboardButton(
                "🚫 🎥 Vídeos — No disponible",
                callback_data="inactive",
            )
        ])

    if muse["calls"]:
        buttons.append([
            InlineKeyboardButton(
                f"✅ 📞 Llamada — {muse['call_price']} 💎/min",
                callback_data="service_call",
            )
        ])
    else:
        buttons.append([
            InlineKeyboardButton(
                "🚫 📞 Llamada — No disponible",
                callback_data="inactive",
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            "⬅️ Volver",
            callback_data="explore",
        )
    ])

    return InlineKeyboardMarkup(buttons)


def muse_profile_text(muse):
    return (
        f"👩🔥 {muse['public_name'].upper()} · "
        f"{muse['age']} AÑOS 🔥👩\n\n"
        f"🔖 @{muse['username']}\n"
        f"{muse['country']}\n\n"
        "✨ Divertida, conversadora y lista para "
        "compartir momentos especiales. 😈\n\n"
        "🟢 Disponible\n\n"
        "💎 SERVICIOS:"
    )


# =========================================================
# MOSTRAR MELISSA
# =========================================================

async def show_melissa(update, context):
    query = update.callback_query
    muse = MELISSA_DEMO

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "💋 Ver perfil",
                callback_data="melissa_profile",
            )
        ],
        [
            InlineKeyboardButton(
                "➡️ Siguiente Musa",
                callback_data="next_muse",
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ Volver",
                callback_data="user",
            )
        ],
    ])

    caption = (
        "🔥💋 DESCUBRE NUESTRAS MUSAS 💋🔥\n\n"
        f"👩 {muse['public_name']} · "
        f"{muse['age']} años · "
        f"{muse['country']}\n\n"
        "✨ Divertida, conversadora y lista para "
        "compartir momentos especiales. 😈\n\n"
        "🟢 Disponible"
    )

    try:
        await query.message.reply_photo(
            photo=muse["photo"],
            caption=caption,
            reply_markup=keyboard,
        )

    except Exception as error:
        print(f"Error mostrando foto: {error}")

        await query.edit_message_text(
            caption,
            reply_markup=keyboard,
        )


# =========================================================
# START
# =========================================================

async def start(update, context):
    context.user_data.pop("registration", None)
    context.user_data.pop("model_login", None)

    t = get_texts(context)

    await update.message.reply_text(
        t["welcome"],
        reply_markup=bottom_menu(t),
    )


# =========================================================
# MENÚ INFERIOR
# =========================================================

async def text_menu(update, context):
    text = update.message.text
    t = get_texts(context)

    # -----------------------------------------------------
    # REGISTRO
    # -----------------------------------------------------

    registration = context.user_data.get("registration")

    if registration:
        await handle_registration_text(
            update,
            context,
        )
        return

    # -----------------------------------------------------
    # LOGIN DE MUSA
    # -----------------------------------------------------

    if context.user_data.get("model_login"):
        await handle_model_login(
            update,
            context,
        )
        return

    # -----------------------------------------------------
    # MENÚ NORMAL
    # -----------------------------------------------------

    if text == t["home"]:
        await start(update, context)
        return

    if text == t["user"]:
        await update.message.reply_text(
            t["user_title"],
            reply_markup=user_menu(t),
        )
        return

    if text == t["model"]:
        await begin_model_access(
            update,
            context,
        )
        return

    if text == t["agency"]:
        await update.message.reply_text(
            t["agency_title"],
            reply_markup=agency_menu(t),
        )
        return

    if text == t["language"]:
        await update.message.reply_text(
            "🌎 Velvet Musa está configurado "
            "en español. 🇪🇸",
            reply_markup=bottom_menu(t),
        )


# =========================================================
# REGISTRO — TEXTO
# =========================================================

async def handle_registration_text(update, context):
    registration = context.user_data.get("registration")

    if not registration:
        return

    text = update.message.text.strip()
    step = registration.get("step")

    # -----------------------------------------------------
    # NOMBRE
    # -----------------------------------------------------

    if step == "name":
        if len(text) < 2 or len(text) > 30:
            await update.message.reply_text(
                "❌ El nombre debe tener entre "
                "2 y 30 caracteres.\n\n"
                "Escribe nuevamente tu nombre público."
            )
            return

        registration["name"] = text
        registration["step"] = "username"

        await update.message.reply_text(
            "✅ Nombre guardado.\n\n"
            "Paso 2 de 5\n\n"
            "🔖 Ahora elige tu nombre de usuario "
            "para Velvet Musa.\n\n"
            "Ejemplo:\n"
            "@Melissa35\n\n"
            "No uses espacios."
        )
        return

    # -----------------------------------------------------
    # USERNAME
    # -----------------------------------------------------

    if step == "username":
        username = text.lstrip("@").strip()

        if (
            len(username) < 3
            or len(username) > 25
            or not username.replace("_", "").isalnum()
        ):
            await update.message.reply_text(
                "❌ Ese usuario no es válido.\n\n"
                "Usa entre 3 y 25 caracteres, "
                "sin espacios.\n\n"
                "Ejemplo: Melissa35"
            )
            return

        username_lower = username.lower()

        for model in DATA["models"].values():
            if model.get("username", "").lower() == username_lower:
                await update.message.reply_text(
                    "❌ Ese nombre de usuario ya está ocupado.\n\n"
                    "Elige otro."
                )
                return

        registration["username"] = username
        registration["step"] = "age"

        await update.message.reply_text(
            "✅ Usuario disponible.\n\n"
            "Paso 3 de 5\n\n"
            "🎂 Escribe tu edad.\n\n"
            "Debes tener 18 años o más."
        )
        return

    # -----------------------------------------------------
    # EDAD
    # -----------------------------------------------------

    if step == "age":
        if not text.isdigit():
            await update.message.reply_text(
                "❌ Escribe solamente tu edad en números."
            )
            return

        age = int(text)

        if age < 18:
            await update.message.reply_text(
                "❌ Para registrarte como Musa debes "
                "tener 18 años o más."
            )
            return

        if age > 100:
            await update.message.reply_text(
                "❌ Introduce una edad válida."
            )
            return

        registration["age"] = age
        registration["step"] = "pin"

        await update.message.reply_text(
            "✅ Edad guardada.\n\n"
            "Paso 4 de 5\n\n"
            "🔐 Crea un PIN de 4 a 6 números.\n\n"
            "Este PIN protegerá tu panel de Musa.\n\n"
            "⚠️ No compartas tu PIN con nadie."
        )
        return

    # -----------------------------------------------------
    # PIN
    # -----------------------------------------------------

    if step == "pin":
        if (
            not text.isdigit()
            or len(text) < 4
            or len(text) > 6
        ):
            await update.message.reply_text(
                "❌ El PIN debe contener entre "
                "4 y 6 números.\n\n"
                "Inténtalo nuevamente."
            )
            return

        registration["pin"] = text
        registration["step"] = "photo"

        await update.message.reply_text(
            "✅ PIN creado de forma segura.\n\n"
            "Paso 5 de 5\n\n"
            "📸 Ahora envíame la foto que quieres "
            "utilizar como perfil de Musa.\n\n"
            "Esta será la foto que podrán ver "
            "los usuarios."
        )
        return


# =========================================================
# REGISTRO — FOTO
# =========================================================

async def handle_registration_photo(update, context):
    registration = context.user_data.get("registration")

    if not registration:
        return

    if registration.get("step") != "photo":
        return

    photo = update.message.photo[-1]

    registration["photo_file_id"] = photo.file_id

    await finish_registration(
        update,
        context,
    )


# =========================================================
# LOGIN DE MUSA
# =========================================================

async def handle_model_login(update, context):
    text = update.message.text.strip()

    if not text.isdigit():
        await update.message.reply_text(
            "❌ El PIN debe contener solamente números."
        )
        return

    if len(text) < 4 or len(text) > 6:
        await update.message.reply_text(
            "❌ El PIN debe tener entre 4 y 6 números."
        )
        return

    user_id = str(update.effective_user.id)
    model = DATA["models"].get(user_id)

    if not model:
        context.user_data.pop("model_login", None)

        await update.message.reply_text(
            "❌ No encontramos tu cuenta de Musa."
        )
        return

    if not verify_pin(
        text,
        model.get("pin_hash", ""),
    ):
        await update.message.reply_text(
            "❌ PIN incorrecto.\n\n"
            "Inténtalo nuevamente."
        )
        return

    context.user_data["model_authenticated"] = True
    context.user_data.pop("model_login", None)

    t = get_texts(context)

    await update.message.reply_text(
        "🔓💋 ACCESO CONCEDIDO 💋🔓\n\n"
        f"Bienvenida, {model['public_name']} 🖤",
        reply_markup=bottom_menu(t),
    )

    await update.message.reply_text(
        t["model_title"],
        reply_markup=model_menu(t),
    )


# =========================================================
# BOTONES
# =========================================================

async def buttons(update, context):
    query = update.callback_query
    data = query.data
    t = get_texts(context)

    await query.answer()

    # =====================================================
    # REGISTRO
    # =====================================================

    if data == "register_model":
        await start_registration(
            update,
            context,
        )
        return

    if data == "cancel_registration":
        context.user_data.pop("registration", None)

        await query.edit_message_text(
            "❌ Registro cancelado.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "⬅️ Volver",
                        callback_data="home",
                    )
                ]
            ]),
        )
        return

    # =====================================================
    # NAVEGACIÓN
    # =====================================================

    if data == "home":
        await query.edit_message_text(
            t["welcome"],
            reply_markup=None,
        )
        return

    if data == "user":
        await query.edit_message_text(
            t["user_title"],
            reply_markup=user_menu(t),
        )
        return

    if data == "model":
        model = get_authenticated_model(
            update,
            context,
        )

        if not model:
            await query.edit_message_text(
                "🔐 Debes iniciar sesión como Musa "
                "para acceder a este panel.",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton(
                            "⬅️ Volver",
                            callback_data="home",
                        )
                    ]
                ]),
            )
            return

        await query.edit_message_text(
            t["model_title"],
            reply_markup=model_menu(t),
        )
        return

    if data == "agency":
        await query.edit_message_text(
            t["agency_title"],
            reply_markup=agency_menu(t),
        )
        return

    # =====================================================
    # EXPLORAR
    # =====================================================

    if data == "explore":
        await show_melissa(
            update,
            context,
        )
        return

    # =====================================================
    # PERFIL MELISSA
    # =====================================================

    if data == "melissa_profile":
        muse = MELISSA_DEMO

        await query.edit_message_text(
            muse_profile_text(muse),
            reply_markup=muse_profile_keyboard(muse),
        )
        return

    # =====================================================
    # SERVICIOS MELISSA
    # =====================================================

    if data == "inactive":
        await query.answer(
            "🚫 Este servicio no está disponible ahora.",
            show_alert=True,
        )
        return

    if data == "service_chat":
        muse = MELISSA_DEMO

        await query.edit_message_text(
            "💬🖤 CHAT CON MELISSA 🖤💬\n\n"
            f"👩 {muse['public_name']}\n"
            f"🔖 @{muse['username']}\n\n"
            f"💎 Precio: {muse['chat_price']} puntos "
            "por mensaje\n\n"
            "El sistema de saldo y chat será activado "
            "en la siguiente etapa.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "⬅️ Volver al perfil",
                        callback_data="melissa_profile",
                    )
                ]
            ]),
        )
        return

    if data == "service_photo":
        await query.answer(
            "📸 Este servicio todavía no está activo.",
            show_alert=True,
        )
        return

    if data == "service_video":
        await query.answer(
            "🎥 Este servicio todavía no está activo.",
            show_alert=True,
        )
        return

    if data == "service_call":
        await query.answer(
            "📞 Este servicio todavía no está activo.",
            show_alert=True,
        )
        return

    # =====================================================
    # SIGUIENTE MUSA
    # =====================================================

    if data == "next_muse":
        await query.edit_message_text(
            "✨🔥 PRÓXIMAMENTE 🔥✨\n\n"
            "Estamos preparando más Musas para "
            "Velvet Musa. 🖤😈",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "⬅️ Volver",
                        callback_data="explore",
                    )
                ]
            ]),
        )
        return

    # =====================================================
    # USUARIO
    # =====================================================

    if data == "balance":
        await query.edit_message_text(
            t["balance_text"],
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        t["recharge"],
                        callback_data="recharge",
                    )
                ],
                [
                    InlineKeyboardButton(
                        t["back"],
                        callback_data="user",
                    )
                ],
            ]),
        )
        return

    if data == "recharge":
        await query.edit_message_text(
            t["coming"],
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        t["back"],
                        callback_data="user",
                    )
                ]
            ]),
        )
        return

    if data == "history":
        await query.edit_message_text(
            t["history_text"],
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        t["back"],
                        callback_data="user",
                    )
                ]
            ]),
        )
        return

    if data in [
        "user_calls",
        "user_profile",
    ]:
        await query.edit_message_text(
            t["coming"],
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        t["back"],
                        callback_data="user",
                    )
                ]
            ]),
        )
        return

    # =====================================================
    # PERFIL DE MUSA AUTENTICADA
    # =====================================================

    if data == "model_profile":
        model = get_authenticated_model(
            update,
            context,
        )

        if not model:
            await query.answer(
                "🔐 Debes iniciar sesión primero.",
                show_alert=True,
            )
            return

        await query.edit_message_text(
            model_profile_text(model),
            reply_markup=model_profile_keyboard(),
        )
        return

    # =====================================================
    # ACTIVAR / DESACTIVAR CHAT
    # =====================================================

    if data == "toggle_chat":
        model = get_authenticated_model(
            update,
            context,
        )

        if not model:
            await query.answer(
                "🔐 Sesión no válida.",
                show_alert=True,
            )
            return

        model["chat"] = not model["chat"]
        save_data(DATA)

        status = (
            "✅ Chat activado"
            if model["chat"]
            else "🚫 Chat desactivado"
        )

        await query.answer(status)

        await query.edit_message_text(
            model_profile_text(model),
            reply_markup=model_profile_keyboard(),
        )
        return

    # =====================================================
    # ACTIVAR / DESACTIVAR FOTOS
    # =====================================================

    if data == "toggle_photos":
        model = get_authenticated_model(
            update,
            context,
        )

        if not model:
            await query.answer(
                "🔐 Sesión no válida.",
                show_alert=True,
            )
            return

        model["photos"] = not model["photos"]
        save_data(DATA)

        status = (
            "✅ Fotos activadas"
            if model["photos"]
            else "🚫 Fotos desactivadas"
        )

        await query.answer(status)

        await query.edit_message_text(
            model_profile_text(model),
            reply_markup=model_profile_keyboard(),
        )
        return

    # =====================================================
    # ACTIVAR / DESACTIVAR VÍDEOS
    # =====================================================

    if data == "toggle_videos":
        model = get_authenticated_model(
            update,
            context,
        )

        if not model:
            await query.answer(
                "🔐 Sesión no válida.",
                show_alert=True,
            )
            return

        model["videos"] = not model["videos"]
        save_data(DATA)

        status = (
            "✅ Vídeos activados"
            if model["videos"]
            else "🚫 Vídeos desactivados"
        )

        await query.answer(status)

        await query.edit_message_text(
            model_profile_text(model),
            reply_markup=model_profile_keyboard(),
        )
        return

    # =====================================================
    # ACTIVAR / DESACTIVAR LLAMADAS
    # =====================================================

    if data == "toggle_calls":
        model = get_authenticated_model(
            update,
            context,
        )

        if not model:
            await query.answer(
                "🔐 Sesión no válida.",
                show_alert=True,
            )
            return

        model["calls"] = not model["calls"]
        save_data(DATA)

        status = (
            "✅ Llamadas activadas"
            if model["calls"]
            else "🚫 Llamadas desactivadas"
        )

        await query.answer(status)

        await query.edit_message_text(
            model_profile_text(model),
            reply_markup=model_profile_keyboard(),
        )
        return

    # =====================================================
    # FUNCIONES MODELO
    # =====================================================

    model_actions = [
        "model_content",
        "publish",
        "earnings",
        "sales",
        "model_calls",
        "my_agency",
        "withdraw",
    ]

    if data in model_actions:
        model = get_authenticated_model(
            update,
            context,
        )

        if not model:
            await query.answer(
                "🔐 Debes iniciar sesión como Musa.",
                show_alert=True,
            )
            return

        await query.edit_message_text(
            t["coming"],
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        t["back"],
                        callback_data="model",
                    )
                ]
            ]),
        )
        return

    # =====================================================
    # AGENCIA
    # =====================================================

    agency_actions = [
        "models",
        "recruit",
        "codes",
        "team_sales",
        "commissions",
        "agency_withdraw",
        "agency_profile",
        "create_agency",
    ]

    if data in agency_actions:
        await query.edit_message_text(
            t["coming"],
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        t["back"],
                        callback_data="agency",
                    )
                ]
            ]),
        )
        return


# =========================================================
# MANEJADOR DE FOTOS
# =========================================================

async def photo_handler(update, context):
    registration = context.user_data.get("registration")

    if registration:
        await handle_registration_photo(
            update,
            context,
        )


# =========================================================
# INICIO DEL BOT
# =========================================================

def main():
    if not TOKEN:
        raise RuntimeError(
            "No se encontró BOT_TOKEN en las variables de entorno."
        )

    Thread(
        target=run_web,
        daemon=True,
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
            start,
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            buttons,
        )
    )

    application.add_handler(
        MessageHandler(
            filters.PHOTO,
            photo_handler,
        )
    )

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            text_menu,
        )
    )

    print(
        "🌟 Velvet Musa: bot iniciado correctamente 🔥"
    )

    application.run_polling()


# =========================================================
# EJECUTAR
# =========================================================

if __name__ == "__main__":
    main()
