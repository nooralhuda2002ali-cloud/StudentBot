import os
import logging

from fastapi import FastAPI, Request
import uvicorn

from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters,
    CommandHandler
)


# =========================
# الإعدادات
# =========================

TOKEN = "8790089235:AAHJWQnDDowpuaU6MI_Xm-AC5jxv9ZopI4g"
ADMIN_ID = 1328541895


# =========================
# Logging
# =========================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)


# =========================
# Telegram Application
# =========================

telegram_app = (
    Application.builder()
    .token(TOKEN)
    .updater(None)
    .build()
)


# =========================
# بداية البوت
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "أهلاً 🌷\n"
        "أرسل رسالتك أو صورة أو ملف وسيتم الرد عليك."
    )


# =========================
# استقبال رسائل الطلاب
# =========================

async def receive_student(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return

    user = update.effective_user

    info = (
        f"📩 رسالة جديدة\n\n"
        f"👤 الاسم: {user.full_name}\n"
        f"🆔 ID: {user.id}\n"
    )

    if user.username:
        info += f"🔹 Username: @{user.username}\n"


    try:

        if update.message.text:

            await context.bot.send_message(
                ADMIN_ID,
                info +
                f"\n💬 الرسالة:\n"
                f"{update.message.text}\n\n"
                f"للرد:\n"
                f"/reply {user.id}"
            )


        elif update.message.photo:

            await context.bot.send_photo(
                ADMIN_ID,
                update.message.photo[-1].file_id,
                caption=
                info +
                f"\n📷 صورة\n\n"
                f"للرد:\n"
                f"/reply {user.id}"
            )


        elif update.message.document:

            await context.bot.send_document(
                ADMIN_ID,
                update.message.document.file_id,
                caption=
                info +
                f"\n📄 ملف\n\n"
                f"للرد:\n"
                f"/reply {user.id}"
            )


        elif update.message.video:

            await context.bot.send_video(
                ADMIN_ID,
                update.message.video.file_id,
                caption=
                info +
                f"\n🎥 فيديو\n\n"
                f"للرد:\n"
                f"/reply {user.id}"
            )


        elif update.message.audio:

            await context.bot.send_audio(
                ADMIN_ID,
                update.message.audio.file_id,
                caption=
                info +
                f"\n🎵 صوت\n\n"
                f"للرد:\n"
                f"/reply {user.id}"
            )


        elif update.message.voice:

            await context.bot.send_voice(
                ADMIN_ID,
                update.message.voice.file_id,
                caption=
                info +
                f"\n🎤 رسالة صوتية\n\n"
                f"للرد:\n"
                f"/reply {user.id}"
            )


        await update.message.reply_text(
            "✅ تم استلام رسالتك"
        )


    except Exception as e:

        logger.exception(
            "Error while sending student message"
        )

        await update.message.reply_text(
            "❌ حدث خطأ أثناء إرسال رسالتك."
        )


# =========================
# أمر الرد
# =========================

async def reply_user(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if update.effective_user.id != ADMIN_ID:
        return


    try:

        user_id = int(
            context.args[0]
        )

        context.user_data[
            "reply_to"
        ] = user_id


        await update.message.reply_text(
            "✅ الآن أرسل الرسالة أو الصورة أو الملف أو الفيديو"
        )


    except:

        await update.message.reply_text(
            "استخدم:\n"
            "/reply ID"
        )


# =========================
# رد الإدارة
# =========================

async def admin_reply(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if update.effective_user.id != ADMIN_ID:
        return


    if not update.message:
        return


    user_id = context.user_data.get(
        "reply_to"
    )


    if not user_id:
        return


    try:

        # النص
        if update.message.text:

            await context.bot.send_message(
                user_id,
                update.message.text
            )


        # الصورة
        elif update.message.photo:

            await context.bot.send_photo(
                user_id,
                update.message.photo[-1].file_id
            )


        # الملف
        elif update.message.document:

            await context.bot.send_document(
                user_id,
                update.message.document.file_id
            )


        # الفيديو
        elif update.message.video:

            await context.bot.send_video(
                user_id,
                update.message.video.file_id
            )


        # الصوت
        elif update.message.audio:

            await context.bot.send_audio(
                user_id,
                update.message.audio.file_id
            )


        # الرسالة الصوتية
        elif update.message.voice:

            await context.bot.send_voice(
                user_id,
                update.message.voice.file_id
            )


        else:

            await update.message.reply_text(
                "❌ هذا النوع من الرسائل غير مدعوم."
            )

            return


        await update.message.reply_text(
            "✅ تم الإرسال"
        )


        context.user_data.pop(
            "reply_to",
            None
        )


    except Exception as e:

        logger.exception(
            "Error while sending admin reply"
        )

        await update.message.reply_text(
            f"❌ حدث خطأ:\n{e}"
        )


# =========================
# الأوامر
# =========================

telegram_app.add_handler(
    CommandHandler(
        "start",
        start
    )
)


telegram_app.add_handler(
    CommandHandler(
        "reply",
        reply_user
    )
)


# =========================
# رسائل الإدارة
# =========================

telegram_app.add_handler(
    MessageHandler(
        filters.ALL
        & ~filters.COMMAND
        & filters.User(ADMIN_ID),
        admin_reply
    )
)


# =========================
# رسائل الطلاب
# =========================

telegram_app.add_handler(
    MessageHandler(
        filters.ALL
        & ~filters.COMMAND
        & ~filters.User(ADMIN_ID),
        receive_student
    )
)


# =========================
# FastAPI
# =========================

web_app = FastAPI()


@web_app.get("/")
async def home():

    return {
        "status": "Bot is running"
    }


@web_app.post("/telegram")
async def telegram_webhook(
    request: Request
):

    data = await request.json()

    update = Update.de_json(
        data,
        telegram_app.bot
    )

    await telegram_app.update_queue.put(
        update
    )

    return {
        "ok": True
    }


# =========================
# تشغيل التطبيق
# =========================

@web_app.on_event("startup")
async def startup():

    await telegram_app.initialize()

    await telegram_app.start()

    render_url = os.environ.get(
        "RENDER_EXTERNAL_URL"
    )

    if not render_url:

        raise RuntimeError(
            "RENDER_EXTERNAL_URL is missing"
        )


    webhook_url = (
        render_url +
        "/telegram"
    )


    await telegram_app.bot.set_webhook(
        url=webhook_url,
        allowed_updates=Update.ALL_TYPES
    )


    logger.info(
        f"Webhook set to: {webhook_url}"
    )


@web_app.on_event("shutdown")
async def shutdown():

    try:

        await telegram_app.bot.delete_webhook()

    except Exception:

        pass


    await telegram_app.stop()

    await telegram_app.shutdown()


# =========================
# تشغيل Web Server
# =========================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            "10000"
        )
    )

    uvicorn.run(
        web_app,
        host="0.0.0.0",
        port=port
    )
