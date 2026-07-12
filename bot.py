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
