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

app_web = Flask(__name__)


@app_web.route("/")
def inicio_web():
    return "🌟 Digitalia está funcionando 🔥"


def iniciar_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host="0.0.0.0", port=port)


# ==================================================
# 📱 MENÚ INFERIOR
# ==================================================

def menu_inferior():

    return ReplyKeyboardMarkup(
        [
            ["🏠 Inicio", "👤 Soy Usuario"],
            ["🔥 Soy Modelo", "🏢 Soy Agencia"],
        ],
        resize_keyboard=True,
        is_persistent=True
    )


# ==================================================
# 🌟 MENÚ PRINCIPAL
# ==================================================

def menu_principal():

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "👤 Soy Usuario",
                callback_data="usuario"
            )
        ],
        [
            InlineKeyboardButton(
                "🔥 Soy Modelo",
                callback_data="modelo"
            )
        ],
        [
            InlineKeyboardButton(
                "🏢 Soy Agencia",
                callback_data="agencia"
            )
        ]
    ])


# ==================================================
# 👋 MENSAJE DE BIENVENIDA
# ==================================================

async def bienvenida(update: Update):

    await update.message.reply_text(
        "🌟🔥 ¡BIENVENIDO A DIGITALIA! 🔥🌟\n\n"

        "💎 Un espacio donde puedes "
        "✨ descubrir, conectar y ganar.\n\n"

        "👤 ¿Buscas contenido y nuevas experiencias?\n"
        "🔎 Explora modelos, descubre perfiles "
        "y desbloquea contenido exclusivo.\n\n"

        "🔥 ¿Quieres ganar dinero?\n"
        "📸 Conviértete en modelo, publica tu contenido "
        "y recibe pagos.\n\n"

        "🏢 ¿Tienes una agencia?\n"
        "👩‍👩‍👧 Recluta modelos, crea tu equipo "
        "y gana comisiones.\n\n"

        "💎 Tú eliges cómo vivir Digitalia.\n\n"

        "👇 Selecciona una opción para comenzar:",
        reply_markup=menu_inferior()
    )

    await update.message.reply_text(
        "✨ ¿Qué quieres hacer?",
        reply_markup=menu_principal()
    )


# ==================================================
# 🚀 START
# ==================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await bienvenida(update)


# ==================================================
# 👤 MENÚ USUARIO
# ==================================================

def menu_usuario():

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔎 Explorar modelos",
                callback_data="explorar"
            )
        ],
        [
            InlineKeyboardButton(
                "⭐ Mi saldo",
                callback_data="saldo"
            )
        ],
        [
            InlineKeyboardButton(
                "💰 Recargar saldo",
                callback_data="recargar"
            )
        ],
        [
            InlineKeyboardButton(
                "🛍️ Mis compras",
                callback_data="compras"
            )
        ],
        [
            InlineKeyboardButton(
                "📞 Mis llamadas",
                callback_data="mis_llamadas"
            )
        ],
        [
            InlineKeyboardButton(
                "👤 Mi perfil",
                callback_data="perfil"
            )
        ]
    ])


# ==================================================
# 🔥 MENÚ MODELO
# ==================================================

def menu_modelo():

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "👤 Mi perfil",
                callback_data="perfil_modelo"
            )
        ],
        [
            InlineKeyboardButton(
                "📸 Mi contenido",
                callback_data="contenido_modelo"
            )
        ],
        [
            InlineKeyboardButton(
                "➕ Publicar contenido",
                callback_data="publicar"
            )
        ],
        [
            InlineKeyboardButton(
                "💰 Mis ganancias",
                callback_data="ganancias"
            )
        ],
        [
            InlineKeyboardButton(
                "📊 Mis ventas",
                callback_data="ventas"
            )
        ],
        [
            InlineKeyboardButton(
                "📞 Mis llamadas",
                callback_data="llamadas_modelo"
            )
        ],
        [
            InlineKeyboardButton(
                "🏢 Mi agencia",
                callback_data="mi_agencia"
            )
        ],
        [
            InlineKeyboardButton(
                "💸 Solicitar retiro",
                callback_data="retiro"
            )
        ]
    ])


# ==================================================
# 🏢 MENÚ AGENCIA
# ==================================================

def menu_agencia():

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "👩‍👩‍👧 Mis modelos",
                callback_data="mis_modelos"
            )
        ],
        [
            InlineKeyboardButton(
                "➕ Reclutar modelo",
                callback_data="reclutar"
            )
        ],
        [
            InlineKeyboardButton(
                "🔑 Mis códigos",
                callback_data="codigos"
            )
        ],
        [
            InlineKeyboardButton(
                "📊 Ventas del equipo",
                callback_data="ventas_equipo"
            )
        ],
        [
            InlineKeyboardButton(
                "💰 Mis comisiones",
                callback_data="comisiones"
            )
        ],
        [
            InlineKeyboardButton(
                "💸 Solicitar retiro",
                callback_data="retiro_agencia"
            )
        ],
        [
            InlineKeyboardButton(
                "📝 Mi agencia",
                callback_data="perfil_agencia"
            )
        ],
        [
            InlineKeyboardButton(
                "🏗️ Crear agencia",
                callback_data="crear_agencia"
            )
        ]
    ])


# ==================================================
# 📱 MENÚ INFERIOR
# ==================================================

async def menu_texto(update: Update, context: ContextTypes.DEFAULT_TYPE):

    texto = update.message.text

    # 🏠 INICIO

    if texto == "🏠 Inicio":

        await update.message.reply_text(
            "🌟🔥 DIGITALIA 🔥🌟\n\n"
            "👋 ¡Qué bueno verte otra vez!\n\n"
            "💎 ¿Qué quieres hacer hoy?",
            reply_markup=menu_principal()
        )

    # 👤 USUARIO

    elif texto == "👤 Soy Usuario":

        await update.message.reply_text(
            "👤💎 ¡MODO USUARIO ACTIVADO! 💎\n\n"
            "🔎 Descubre modelos\n"
            "⭐ Consulta tu saldo\n"
            "💰 Recarga puntos\n"
            "🛍️ Revisa tus compras\n"
            "📞 Gestiona tus llamadas\n\n"
            "👇 ¿Qué quieres hacer?",
            reply_markup=menu_usuario()
        )

    # 🔥 MODELO

    elif texto == "🔥 Soy Modelo":

        await update.message.reply_text(
            "🔥💎 ¡MODO MODELO! 💎🔥\n\n"
            "📸 Publica contenido\n"
            "💬 Conecta con usuarios\n"
            "📞 Recibe llamadas\n"
            "💰 Gana dinero\n"
            "📊 Controla tus ventas\n"
            "💸 Solicita tus retiros\n\n"
            "👇 Gestiona tu actividad:",
            reply_markup=menu_modelo()
        )

    # 🏢 AGENCIA

    elif texto == "🏢 Soy Agencia":

        await update.message.reply_text(
            "🏢🔥 ¡MODO AGENCIA! 🔥🏢\n\n"
            "👩‍👩‍👧 Gestiona tus modelos\n"
            "➕ Recluta nuevas modelos\n"
            "🔑 Administra tus códigos\n"
            "📊 Controla las ventas\n"
            "💰 Consulta tus comisiones\n"
            "💸 Gestiona tus retiros\n\n"
            "👇 Gestiona tu agencia:",
            reply_markup=menu_agencia()
        )


# ==================================================
# 🔘 BOTONES INTERNOS
# ==================================================

async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    # 👤 USUARIO

    if query.data == "usuario":

        await query.edit_message_text(
            "👤💎 ¡MODO USUARIO! 💎\n\n"
            "🔎 Explora modelos\n"
            "⭐ Consulta tu saldo\n"
            "💰 Recarga\n"
            "🛍️ Revisa tus compras\n"
            "📞 Gestiona tus llamadas\n\n"
            "👇 Selecciona una opción:",
            reply_markup=menu_usuario()
        )

    # 🔥 MODELO

    elif query.data == "modelo":

        await query.edit_message_text(
            "🔥💎 ¡MODO MODELO! 💎🔥\n\n"
            "📸 Publica contenido\n"
            "💰 Consulta tus ganancias\n"
            "📊 Revisa tus ventas\n"
            "📞 Gestiona tus llamadas\n"
            "🏢 Consulta tu agencia\n"
            "💸 Solicita tu retiro\n\n"
            "👇 Selecciona una opción:",
            reply_markup=menu_modelo()
        )

    # 🏢 AGENCIA

    elif query.data == "agencia":

        await query.edit_message_text(
            "🏢🔥 ¡MODO AGENCIA! 🔥🏢\n\n"
            "👩‍👩‍👧 Gestiona modelos\n"
            "➕ Recluta modelos\n"
            "🔑 Administra códigos\n"
            "📊 Controla ventas\n"
            "💰 Consulta comisiones\n"
            "🏗️ Crea tu agencia\n\n"
            "👇 Selecciona una opción:",
            reply_markup=menu_agencia()
        )

    # 🔎 EXPLORAR

    elif query.data == "explorar":

        await query.edit_message_text(
            "🔎🔥 MODELOS DISPONIBLES 🔥\n\n"
            "👩 Ana\n"
            "💎 Contenido exclusivo\n"
            "📸 Desde 300 puntos\n\n"
            "👇 Selecciona un perfil:",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "👩 Ana — Ver perfil",
                        callback_data="ana"
                    )
                ]
            ])
        )

    # 👩 ANA

    elif query.data == "ana":

        await query.edit_message_text(
            "👩🔥 ANA 🔥\n\n"
            "💎 Perfil exclusivo\n\n"
            "📸 Foto — 300 puntos\n"
            "🎥 Video — 700 puntos\n"
            "📞 Tiempo privado — 20 puntos/min\n\n"
            "👇 Elige una opción:",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "📸 Foto — 300 puntos",
                        callback_data="foto"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🎥 Video — 700 puntos",
                        callback_data="video"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📞 Tiempo privado",
                        callback_data="llamada"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "⬅️ Volver",
                        callback_data="explorar"
                    )
                ]
            ])
        )

    # 📸 FOTO

    elif query.data == "foto":

        await query.edit_message_text(
            "📸🔥 FOTO EXCLUSIVA\n\n"
            "💎 Precio: 300 puntos\n\n"
            "🔒 Contenido bloqueado.\n"
            "💰 Recarga tu saldo para desbloquearlo.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "💰 Recargar",
                        callback_data="recargar"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "⬅️ Volver",
                        callback_data="ana"
                    )
                ]
            ])
        )

    # 🎥 VIDEO

    elif query.data == "video":

        await query.edit_message_text(
            "🎥🔥 VIDEO EXCLUSIVO\n\n"
            "💎 Precio: 700 puntos\n\n"
            "🔒 Contenido bloqueado.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "💰 Recargar",
                        callback_data="recargar"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "⬅️ Volver",
                        callback_data="ana"
                    )
                ]
            ])
        )

    # 📞 LLAMADA

    elif query.data == "llamada":

        await query.edit_message_text(
            "📞🔥 TIEMPO PRIVADO\n\n"
            "💎 20 puntos por minuto\n\n"
            "🔒 Próximamente podrás solicitar una llamada.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "⬅️ Volver",
                        callback_data="ana"
                    )
                ]
            ])
        )

    # ⭐ SALDO

    elif query.data == "saldo":

        await query.edit_message_text(
            "⭐💰 MI SALDO\n\n"
            "💎 Saldo disponible: 0 puntos\n\n"
            "👇 ¿Quieres recargar?",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "💰 Recargar saldo",
                        callback_data="recargar"
                    )
                ]
            ])
        )

    # 💰 RECARGAR

    elif query.data == "recargar":

        await query.edit_message_text(
            "💰🔥 RECARGAR SALDO\n\n"
            "💎 Próximamente podrás comprar puntos "
            "para desbloquear contenido.\n\n"
            "✨ Digitalia"
        )

    # 🛍️ COMPRAS

    elif query.data == "compras":

        await query.edit_message_text(
            "🛍️💎 MIS COMPRAS\n\n"
            "Todavía no tienes compras."
        )

    # 📞 MIS LLAMADAS

    elif query.data == "mis_llamadas":

        await query.edit_message_text(
            "📞🔥 MIS LLAMADAS\n\n"
            "No tienes llamadas programadas."
        )

    # 👤 PERFIL

    elif query.data == "perfil":

        await query.edit_message_text(
            "👤💎 MI PERFIL\n\n"
            "Tu perfil de usuario está activo."
        )

    # 🔥 OPCIONES MODELO

    elif query.data in [
        "perfil_modelo",
        "contenido_modelo",
        "publicar",
        "ganancias",
        "ventas",
        "llamadas_modelo",
        "mi_agencia",
        "retiro"
    ]:

        await query.edit_message_text(
            "🔥💎 FUNCIÓN DE MODELO\n\n"
            "Esta función formará parte del panel "
            "de modelos de Digitalia.\n\n"
            "🚀 La estamos preparando."
        )

    # 🏢 OPCIONES AGENCIA

    elif query.data in [
        "mis_modelos",
        "reclutar",
        "codigos",
        "ventas_equipo",
        "comisiones",
        "retiro_agencia",
        "perfil_agencia",
        "crear_agencia"
    ]:

        await query.edit_message_text(
            "🏢🔥 PANEL DE AGENCIA\n\n"
            "Esta función formará parte del sistema "
            "de agencias de Digitalia.\n\n"
            "🚀 La estamos preparando."
        )


# ==================================================
# 🚀 INICIAR
# ==================================================

def main():

    Thread(
        target=iniciar_web,
        daemon=True
    ).start()

    application = Application.builder().token(TOKEN).build()

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CallbackQueryHandler(botones)
    )

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            menu_texto
        )
    )

    print("🌟 Digitalia: bot iniciado correctamente 🔥")

    application.run_polling()


if __name__ == "__main__":
    main()
