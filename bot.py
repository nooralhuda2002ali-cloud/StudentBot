from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters,
    CommandHandler
)


TOKEN = "ضعي_التوكن_هنا"
ADMIN_ID = 1328541895


# بداية البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "أهلاً 🌷\n"
        "أرسل رسالتك أو صورة أو ملف وسيتم الرد عليك."
    )


# استقبال رسائل الطلاب
async def receive_student(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    info = (
        f"📩 رسالة جديدة\n\n"
        f"👤 الاسم: {user.full_name}\n"
        f"🆔 ID: {user.id}\n"
    )

    if user.username:
        info += f"🔹 Username: @{user.username}\n"


    if update.message.text:

        await context.bot.send_message(
            ADMIN_ID,
            info +
            f"\n💬 الرسالة:\n{update.message.text}\n\n"
            f"للرد:\n/reply {user.id}"
        )


    elif update.message.photo:

        await context.bot.send_photo(
            ADMIN_ID,
            update.message.photo[-1].file_id,
            caption=info +
            f"\n📷 صورة\n\nللرد:\n/reply {user.id}"
        )


    elif update.message.document:

        await context.bot.send_document(
            ADMIN_ID,
            update.message.document.file_id,
            caption=info +
            f"\n📄 ملف\n\nللرد:\n/reply {user.id}"
        )


    elif update.message.video:

        await context.bot.send_video(
            ADMIN_ID,
            update.message.video.file_id,
            caption=info +
            f"\n🎥 فيديو\n\nللرد:\n/reply {user.id}"
        )


    elif update.message.audio:

        await context.bot.send_audio(
            ADMIN_ID,
            update.message.audio.file_id,
            caption=info +
            f"\n🎵 صوت\n\nللرد:\n/reply {user.id}"
        )


    await update.message.reply_text(
        "✅ تم استلام رسالتك"
    )



# أمر الرد
async def reply_user(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    try:

        user_id = int(context.args[0])

        context.user_data["reply_to"] = user_id

        await update.message.reply_text(
            "✅ أرسل الآن الرسالة أو الصورة أو الملف أو الفيديو"
        )

    except:

        await update.message.reply_text(
            "استخدم:\n/reply ID"
        )



# استقبال رد الإدارة
async def admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return


    user_id = context.user_data.get("reply_to")


    if not user_id:
        return


    if update.message.text:

        await context.bot.send_message(
            user_id,
            update.message.text
        )


    elif update.message.photo:

        await context.bot.send_photo(
            user_id,
            update.message.photo[-1].file_id
        )


    elif update.message.document:

        await context.bot.send_document(
            user_id,
            update.message.document.file_id
        )


    elif update.message.video:

        await context.bot.send_video(
            user_id,
            update.message.video.file_id
        )


    elif update.message.audio:

        await context.bot.send_audio(
            user_id,
            update.message.audio.file_id
        )


    await update.message.reply_text(
        "✅ تم الإرسال"
    )


    context.user_data.pop("reply_to", None)



# تشغيل البوت
app = Application.builder().token(TOKEN).build()


app.add_handler(
    CommandHandler("start", start)
)


app.add_handler(
    CommandHandler("reply", reply_user)
)


# رد الإدارة (نخليه قبل استقبال الطلاب)
app.add_handler(
    MessageHandler(
        filters.ALL & ~filters.COMMAND,
        admin_reply
    )
)


# استقبال الطلاب
app.add_handler(
    MessageHandler(
        (
            filters.TEXT |
            filters.PHOTO |
            filters.Document.ALL |
            filters.VIDEO |
            filters.AUDIO
        )
        & ~filters.COMMAND,
        receive_student
    )
)


app.run_polling()
