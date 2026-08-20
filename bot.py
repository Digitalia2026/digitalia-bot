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
    return "Digitalia está funcionando."


def iniciar_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host="0.0.0.0", port=port)


# =========================
# MENÚ INFERIOR DE TELEGRAM
# =========================

def menu_inferior():
    return ReplyKeyboardMarkup(
        [
            ["🏠 Inicio", "👩 Creadoras", "💰 Saldo"],
            ["🛒 Compras", "👤 Mi cuenta"],
        ],
        resize_keyboard=True,
        is_persistent=True
    )


# =========================
# MENÚ PRINCIPAL
# =========================

def menu_principal():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "👩‍💻 Quiero ser creadora",
                callback_data="creadora"
            )
        ],
        [
            InlineKeyboardButton(
                "🏢 Soy agencia",
                callback_data="agencia"
            )
        ],
        [
            InlineKeyboardButton(
                "💰 Recargar",
                callback_data="recargar"
            )
        ],
        [
            InlineKeyboardButton(
                "❓ Ayuda",
                callback_data="ayuda"
            )
        ],
    ])


async def mostrar_inicio(query):

    await query.edit_message_text(
        "🌟 DIGITALIA\n\n"
        "👋 Bienvenido.\n\n"
        "Compra contenido exclusivo, "
        "descubre creadoras y próximamente "
        "podrás interactuar con ellas.",
        reply_markup=menu_principal()
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🌟 DIGITALIA\n\n"
        "👋 Bienvenido.\n\n"
        "Usa el menú de abajo para navegar por Digitalia.",
        reply_markup=menu_inferior()
    )

    await update.message.reply_text(
        "Selecciona una opción:",
        reply_markup=menu_principal()
    )


# =========================
# MENÚ INFERIOR
# =========================

async def menu_texto(update: Update, context: ContextTypes.DEFAULT_TYPE):

    texto = update.message.text

    if texto == "🏠 Inicio":

        await update.message.reply_text(
            "🌟 DIGITALIA\n\n"
            "👋 Bienvenido.\n\n"
            "Selecciona una opción:",
            reply_markup=menu_principal()
        )

    elif texto == "👩 Creadoras":

        botones_creadoras = [
            [
                InlineKeyboardButton(
                    "👩 Ana — Desde 300 puntos",
                    callback_data="ana"
                )
            ],
            [
                InlineKeyboardButton(
                    "👩‍💻 Quiero ser creadora",
                    callback_data="creadora"
                )
            ]
        ]

        await update.message.reply_text(
            "🌟 CREADORAS DISPONIBLES\n\n"
            "Selecciona una creadora:",
            reply_markup=InlineKeyboardMarkup(botones_creadoras)
        )

    elif texto == "💰 Saldo":

        await update.message.reply_text(
            "⭐ MI SALDO\n\n"
            "Saldo actual: 0 puntos.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "💰 Recargar",
                        callback_data="recargar"
                    )
                ]
            ])
        )

    elif texto == "🛒 Compras":

        await update.message.reply_text(
            "🛒 MIS COMPRAS\n\n"
            "Todavía no tienes compras."
        )

    elif texto == "👤 Mi cuenta":

        await update.message.reply_text(
            "👤 MI CUENTA\n\n"
            "Tu cuenta de Digitalia está activa."
        )


# =========================
# BOTONES INTERNOS
# =========================

async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    # CREADORAS

    if query.data == "creadora":

        await query.edit_message_text(
            "👩‍💻 QUIERO SER CREADORA\n\n"
            "Para registrarte necesitarás pertenecer "
            "a una agencia oficial de Digitalia.\n\n"
            "La agencia te proporcionará un código "
            "de registro.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🔑 Tengo código de agencia",
                        callback_data="codigo_agencia"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🏢 Necesito una agencia",
                        callback_data="buscar_agencia"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "⬅️ Volver",
                        callback_data="inicio"
                    )
                ]
            ])
        )

    # AGENCIA

    elif query.data == "agencia":

        await query.edit_message_text(
            "🏢 PROGRAMA DE AGENCIAS DIGITALIA\n\n"
            "Las agencias podrán incorporar creadoras, "
            "gestionar su equipo y recibir comisiones "
            "por las ventas de sus creadoras.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🔑 Tengo código de agencia",
                        callback_data="login_agencia"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📝 Solicitar ser agencia",
                        callback_data="solicitar_agencia"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "⬅️ Volver",
                        callback_data="inicio"
                    )
                ]
            ])
        )

    # ANA

    elif query.data == "ana":

        await query.edit_message_text(
            "👩 ANA\n\n"
            "✨ Contenido exclusivo\n\n"
            "📸 Foto — 300 puntos\n"
            "🎥 Video — 700 puntos\n"
            "📞 Tiempo privado — 20 puntos/min",
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

    # EXPLORAR

    elif query.data == "explorar":

        await query.edit_message_text(
            "🌟 CREADORAS DISPONIBLES\n\n"
            "👩 Ana\n"
            "✨ Contenido exclusivo\n"
            "💰 Desde 300 puntos",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "👩 Ana — Ver perfil",
                        callback_data="ana"
                    )
                ]
            ])
        )

    # FOTO

    elif query.data == "foto":

        await query.edit_message_text(
            "📸 FOTO DE ANA\n\n"
            "💰 Precio: 300 puntos\n\n"
            "🔓 Próximamente podrás desbloquearla.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "⬅️ Volver al perfil",
                        callback_data="ana"
                    )
                ]
            ])
        )

    # VIDEO

    elif query.data == "video":

        await query.edit_message_text(
            "🎥 VIDEO DE ANA\n\n"
            "💰 Precio: 700 puntos\n\n"
            "🔓 Próximamente podrás desbloquearlo.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "⬅️ Volver al perfil",
                        callback_data="ana"
                    )
                ]
            ])
        )

    # LLAMADA

    elif query.data == "llamada":

        await query.edit_message_text(
            "📞 TIEMPO PRIVADO\n\n"
            "💰 Precio: 20 puntos por minuto\n\n"
            "🔓 Próximamente podrás solicitarlo.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "⬅️ Volver al perfil",
                        callback_data="ana"
                    )
                ]
            ])
        )

    # CÓDIGO AGENCIA

    elif query.data == "codigo_agencia":

        await query.edit_message_text(
            "🔑 CÓDIGO DE AGENCIA\n\n"
            "Escribe el código que te proporcionó "
            "tu agencia.\n\n"
            "Ejemplo: DIGI-4827\n\n"
            "Esta función estará disponible próximamente.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "⬅️ Volver",
                        callback_data="creadora"
                    )
                ]
            ])
        )

    # BUSCAR AGENCIA

    elif query.data == "buscar_agencia":

        await query.edit_message_text(
            "🏢 AGENCIAS OFICIALES\n\n"
            "Aquí aparecerán las agencias oficiales "
            "de Digitalia.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "⬅️ Volver",
                        callback_data="creadora"
                    )
                ]
            ])
        )

    # LOGIN AGENCIA

    elif query.data == "login_agencia":

        await query.edit_message_text(
            "🔑 ACCESO DE AGENCIA\n\n"
            "Introduce tu código de agencia.\n\n"
            "Ejemplo: AGENCIA-1001\n\n"
            "Esta función estará disponible próximamente.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "⬅️ Volver",
                        callback_data="agencia"
                    )
                ]
            ])
        )

    # SOLICITAR AGENCIA

    elif query.data == "solicitar_agencia":

        await query.edit_message_text(
            "📝 SOLICITUD DE AGENCIA\n\n"
            "Las solicitudes serán revisadas por Digitalia "
            "antes de aprobar una nueva agencia.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "⬅️ Volver",
                        callback_data="agencia"
                    )
                ]
            ])
        )

    # RECARGAR

    elif query.data == "recargar":

        await query.edit_message_text(
            "💰 RECARGAR\n\n"
            "La recarga estará disponible próximamente.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "⬅️ Volver",
                        callback_data="inicio"
                    )
                ]
            ])
        )

    # AYUDA

    elif query.data == "ayuda":

        await query.edit_message_text(
            "❓ AYUDA\n\n"
            "Digitalia está actualmente en fase de prueba.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "⬅️ Volver",
                        callback_data="inicio"
                    )
                ]
            ])
        )

    # INICIO

    elif query.data == "inicio":

        await mostrar_inicio(query)


# =========================
# INICIAR DIGITALIA
# =========================

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

    print("Digitalia: bot iniciado correctamente.")

    application.run_polling()


if __name__ == "__main__":
    main()
