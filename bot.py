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


# =========================
# MENÚ PRINCIPAL
# =========================

def menu_principal():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👩 Explorar creadoras", callback_data="explorar")],
        [InlineKeyboardButton("👩‍💻 Quiero ser creadora", callback_data="creadora")],
        [InlineKeyboardButton("🏢 Soy agencia", callback_data="agencia")],
        [InlineKeyboardButton("⭐ Mi saldo", callback_data="saldo")],
        [InlineKeyboardButton("🛒 Mis compras", callback_data="compras")],
        [InlineKeyboardButton("👤 Mi cuenta", callback_data="cuenta")],
        [InlineKeyboardButton("💰 Recargar", callback_data="recargar")],
        [InlineKeyboardButton("❓ Ayuda", callback_data="ayuda")],
    ])


async def mostrar_inicio(query):
    await query.edit_message_text(
        "🌟 DIGITALIA\n\n"
        "👋 Bienvenido.\n"
        "Explora creadoras y descubre contenido exclusivo.",
        reply_markup=menu_principal()
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🌟 DIGITALIA\n\n"
        "👋 Bienvenido.\n"
        "Explora creadoras y descubre contenido exclusivo.",
        reply_markup=menu_principal()
    )


# =========================
# BOTONES
# =========================

async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    # =========================
    # EXPLORAR CREADORAS
    # =========================

    if query.data == "explorar":

        botones_creadoras = [
            [
                InlineKeyboardButton(
                    "👩 Ana — Desde 300 puntos",
                    callback_data="ana"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Volver",
                    callback_data="inicio"
                )
            ],
        ]

        await query.edit_message_text(
            "🌟 CREADORAS DISPONIBLES\n\n"
            "👩 Ana\n"
            "✨ Contenido exclusivo\n"
            "💰 Desde 300 puntos",
            reply_markup=InlineKeyboardMarkup(botones_creadoras)
        )

    # =========================
    # PERFIL ANA
    # =========================

    elif query.data == "ana":

        botones_ana = [
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
                    "📞 Tiempo privado — 20 puntos/min",
                    callback_data="llamada"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Volver",
                    callback_data="explorar"
                )
            ],
        ]

        await query.edit_message_text(
            "👩 ANA\n\n"
            "✨ Contenido exclusivo\n\n"
            "📸 Foto — 300 puntos\n"
            "🎥 Video — 700 puntos\n"
            "📞 Tiempo privado — 20 puntos/min\n\n"
            "Selecciona una opción:",
            reply_markup=InlineKeyboardMarkup(botones_ana)
        )

    # =========================
    # FOTO
    # =========================

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

    # =========================
    # VIDEO
    # =========================

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

    # =========================
    # LLAMADA
    # =========================

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

    # =========================
    # QUIERO SER CREADORA
    # =========================

    elif query.data == "creadora":

        botones_creadora = [
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
            ],
        ]

        await query.edit_message_text(
            "👩‍💻 QUIERO SER CREADORA\n\n"
            "Para registrarte necesitas pertenecer "
            "a una agencia oficial de Digitalia.\n\n"
            "La agencia te proporcionará un código "
            "de registro.",
            reply_markup=InlineKeyboardMarkup(botones_creadora)
        )

    # =========================
    # CÓDIGO DE AGENCIA
    # =========================

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

    # =========================
    # BUSCAR AGENCIA
    # =========================

    elif query.data == "buscar_agencia":

        await query.edit_message_text(
            "🏢 AGENCIAS OFICIALES\n\n"
            "Aquí aparecerán las agencias oficiales "
            "de Digitalia.\n\n"
            "Próximamente podrás elegir una agencia "
            "y contactar con ella.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "⬅️ Volver",
                        callback_data="creadora"
                    )
                ]
            ])
        )

    # =========================
    # SOY AGENCIA
    # =========================

    elif query.data == "agencia":

        botones_agencia = [
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
            ],
        ]

        await query.edit_message_text(
            "🏢 PROGRAMA DE AGENCIAS DIGITALIA\n\n"
            "Las agencias podrán incorporar creadoras, "
            "gestionar su equipo y recibir comisiones "
            "por las ventas de sus creadoras.",
            reply_markup=InlineKeyboardMarkup(botones_agencia)
        )

    # =========================
    # ACCESO AGENCIA
    # =========================

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

    # =========================
    # SOLICITAR AGENCIA
    # =========================

    elif query.data == "solicitar_agencia":

        await query.edit_message_text(
            "📝 SOLICITUD DE AGENCIA\n\n"
            "Las solicitudes serán revisadas por Digitalia "
            "antes de aprobar una nueva agencia.\n\n"
            "Próximamente podrás enviar tu solicitud.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "⬅️ Volver",
                        callback_data="agencia"
                    )
                ]
            ])
        )

    # =========================
    # SALDO
    # =========================

    elif query.data == "saldo":

        await query.edit_message_text(
            "⭐ TU SALDO\n\n"
            "Saldo actual: 0 puntos.",
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
                        callback_data="inicio"
                    )
                ]
            ])
        )

    # =========================
    # COMPRAS
    # =========================

    elif query.data == "compras":

        await query.edit_message_text(
            "🛒 MIS COMPRAS\n\n"
            "Todavía no tienes compras.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "⬅️ Volver",
                        callback_data="inicio"
                    )
                ]
            ])
        )

    # =========================
    # CUENTA
    # =========================

    elif query.data == "cuenta":

        await query.edit_message_text(
            "👤 MI CUENTA\n\n"
            "Tu cuenta de Digitalia está activa.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "⬅️ Volver",
                        callback_data="inicio"
                    )
                ]
            ])
        )

    # =========================
    # RECARGAR
    # =========================

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

    # =========================
    # AYUDA
    # =========================

    elif query.data == "ayuda":

        await query.edit_message_text(
            "❓ AYUDA\n\n"
            "Digitalia está en fase de prueba.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "⬅️ Volver",
                        callback_data="inicio"
                    )
                ]
            ])
        )

    # =========================
    # VOLVER AL INICIO
    # =========================

    elif query.data == "inicio":

        await mostrar_inicio(query)


# =========================
# INICIAR BOT
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

    print("Digitalia: bot iniciado correctamente.")

    application.run_polling()


if __name__ == "__main__":
    main()
