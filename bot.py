import os
from threading import Thread

from flask import Flask
from telegram import Update, ReplyKeyboardMarkup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler
from telegram.ext import MessageHandler, CallbackQueryHandler
from telegram.ext import ContextTypes, filters


TOKEN = os.getenv("BOT_TOKEN")

# =========================================================
# CONFIGURACIÓN DE VELVET MUSA
# =========================================================

MELISSA_PHOTO_URL = (
    "https://i.ibb.co/VYpN8wtP/"
    "Chat-GPT-Image-1-ago-2026-06-35-15-p-m.png"
)

MODELS_CHANNEL = "https://t.me/+BUxwqByLYK00ZTYx"
AGENCY_CHANNEL = "https://t.me/+MrTIOV4GlqAzNWIx"


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
# TEXTOS EN ESPAÑOL
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

    "user_title": (
        "👤💎 MODO USUARIO 💎👤"
    ),

    "explore": "🔎 Explorar Musas",
    "balance": "⭐ Mi saldo",
    "recharge": "💰 Recargar saldo",
    "history": "📜 Historial",
    "calls": "📞 Mis llamadas",
    "profile": "👤 Mi perfil",

    "model_title": (
        "🔥💋 MODO MODELO 💋🔥"
    ),

    "model_profile": "👤 Mi perfil",
    "content": "📸 Mi contenido",
    "publish": "➕ Publicar contenido",
    "earnings": "💰 Mis ganancias",
    "sales": "📊 Mis ventas",
    "model_calls": "📞 Mis llamadas",
    "my_agency": "🏢 Mi agencia",
    "withdraw": "💸 Solicitar retiro",
    "model_channel": "📢 Canal exclusivo de Musas",

    "agency_title": (
        "🏢🔥 MODO AGENCIA 🔥🏢"
    ),

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
# TEXTOS EN INGLÉS
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

    "user_title": (
        "👤💎 USER MODE 💎👤"
    ),

    "explore": "🔎 Explore Muses",
    "balance": "⭐ My balance",
    "recharge": "💰 Add balance",
    "history": "📜 History",
    "calls": "📞 My calls",
    "profile": "👤 My profile",

    "model_title": (
        "🔥💋 MODEL MODE 💋🔥"
    ),

    "model_profile": "👤 My profile",
    "content": "📸 My content",
    "publish": "➕ Publish content",
    "earnings": "💰 My earnings",
    "sales": "📊 My sales",
    "model_calls": "📞 My calls",
    "my_agency": "🏢 My agency",
    "withdraw": "💸 Request withdrawal",
    "model_channel": "📢 Exclusive Muses channel",

    "agency_title": (
        "🏢🔥 AGENCY MODE 🔥🏢"
    ),

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
# START
# =========================================================

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


# =========================================================
# MENÚ INFERIOR
# =========================================================

async def text_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
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
# MOSTRAR MELISSA
# =========================================================

async def show_melissa(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
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
        "📞 25 💎/min"
    )

    try:
        await query.message.reply_photo(
            photo=MELISSA_PHOTO_URL,
            caption=caption,
            reply_markup=menu
        )

        await query.edit_message_text(
            "📸 Melissa está aquí arriba 👆🔥"
        )

    except Exception:
        await query.edit_message_text(
            caption,
            reply_markup=menu
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

    if data == "explore":
        await show_melissa(update, context)
        return

    if data == "melissa_profile":
        await query.edit_message_text(
            "👩🔥 MELISSA · 35 AÑOS 🔥👩\n\n"
            "🇨🇴 Colombia\n\n"
            "✨ Me encanta conversar, conocer personas "
            "y compartir momentos especiales. 😈\n\n"
            "🟢 Disponible\n"
            "📞 25 💎 por minuto\n"
            "📸 Contenido exclusivo",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "📸 Contenido exclusivo",
                        callback_data="melissa_content"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📞 Solicitar llamada",
                        callback_data="melissa_call"
                    )
                ],
                [
                    InlineKeyboardButton(
                        t["back"],
                        callback_data="explore"
                    )
                ]
            ])
        )
        return

    if data == "melissa_content":
        await query.edit_message_text(
            "🔒📸 CONTENIDO EXCLUSIVO 📸🔒\n\n"
            "💎 Este contenido será accesible mediante "
            "puntos cuando activemos el sistema de pagos.\n\n"
            "🔐 Las fotos privadas no aparecerán en "
            "el perfil público.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        t["back"],
                        callback_data="melissa_profile"
                    )
                ]
            ])
        )
        return

    if data == "melissa_call":
        await query.edit_message_text(
            "📞🔥 LLAMADA PRIVADA 🔥📞\n\n"
            "👩 Melissa\n"
            "💎 25 puntos por minuto\n\n"
            "😈 Las llamadas estarán disponibles "
            "cuando activemos el sistema de llamadas.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        t["back"],
                        callback_data="melissa_profile"
                    )
                ]
            ])
        )
        return

    if data == "next_muse":
        await query.edit_message_text(
            "✨🔥 PRÓXIMAMENTE 🔥✨\n\n"
            "Estamos preparando más Musas para "
            "Velvet Musa. 😈\n\n"
            "👩 Melissa es nuestra primera Musa "
            "de prueba.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        t["back"],
                        callback_data="explore"
                    )
                ]
            ])
        )
        return

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

    model_actions = [
        "model_profile",
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


# =========================================================
# INICIO DEL BOT
# =========================================================

def main():
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
            filters.TEXT & ~filters.COMMAND,
            text_menu
        )
    )

    print(
        "🌟 Velvet Musa: bot iniciado correctamente 🔥"
    )

    application.run_polling()


if __name__ == "__main__":
    main()
