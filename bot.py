from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters,
    CommandHandler
)

TOKEN = "8790089235:AAGtgJFfn3k8sffWfkFQSza0C0vV3aMzhWc"
ADMIN_ID = 1328541895


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلاً بك 🌷\n"
        "أرسل رسالتك أو صورة أو ملف، وسيتم الرد عليك."
    )


async def send_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    info = (
        f"📩 رسالة جديدة\n\n"
        f"👤 الاسم: {user.full_name}\n"
        f"🆔 ID: {user.id}\n"
    )

    if user.username:
        info += f"🔹 Username: @{user.username}\n"


    # رسالة نصية
    if update.message.text:

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=info + 
            f"\n💬 الرسالة:\n{update.message.text}\n\n"
            f"للرد:\n/reply {user.id} الرسالة"
        )


    # صورة
    elif update.message.photo:

        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=update.message.photo[-1].file_id,
            caption=info +
            f"\n📷 صورة\n\nللرد:\n/reply {user.id} الرسالة"
        )


    # ملف PDF / Word / أي ملف
    elif update.message.document:

        await context.bot.send_document(
            chat_id=ADMIN_ID,
            document=update.message.document.file_id,
            caption=info +
            f"\n📄 ملف\n\nللرد:\n/reply {user.id} الرسالة"
        )
        # فيديو
async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    await context.bot.send_video(
        chat_id=ADMIN_ID,
        video=update.message.video.file_id,
        caption=(
            f"🎥 فيديو جديد\n\n"
            f"👤 الاسم: {user.full_name}\n"
            f"🆔 ID: {user.id}\n\n"
            f"للرد:\n/reply {user.id} الرسالة"
        )
    )


# صوت / تسجيل
async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    await context.bot.send_audio(
        chat_id=ADMIN_ID,
        audio=update.message.audio.file_id,
        caption=(
            f"🎵 ملف صوتي جديد\n\n"
            f"👤 الاسم: {user.full_name}\n"
            f"🆔 ID: {user.id}\n\n"
            f"للرد:\n/reply {user.id} الرسالة"
        )
    )


# الرد على الطالب
async def reply_user(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    try:
        user_id = int(context.args[0])
        text = " ".join(context.args[1:])

        await context.bot.send_message(
            chat_id=user_id,
            text=text
        )

        await update.message.reply_text(
            "✅ تم إرسال الرد"
        )

    except:
        await update.message.reply_text(
            "استخدم:\n/reply ID الرسالة"
        )
app = Application.builder().token(TOKEN).build()


# الأوامر
app.add_handler(
    CommandHandler("start", start)
)

app.add_handler(
    CommandHandler("reply", reply_user)
)


# النصوص + الصور + الملفات
app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        send_to_admin
    )
)

app.add_handler(
    MessageHandler(
        filters.PHOTO,
        send_to_admin
    )
)

app.add_handler(
    MessageHandler(
        filters.Document.ALL,
        send_to_admin
    )
)


# الفيديو
app.add_handler(
    MessageHandler(
        filters.VIDEO,
        handle_video
    )
)


# الصوت
app.add_handler(
    MessageHandler(
        filters.AUDIO,
        handle_audio
    )
)


# تشغيل البوت
app.run_polling()
