from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters, CommandHandler

TOKEN =8790089235:AAGtgJFfn3k8sffWfkFQSza0C0vV3aMzhWc
ADMIN_ID = 0

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome 🌷\nSend your message and you will get a reply."
    )

async def receive_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.message.text

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"New message\n\n"
             f"Name: {user.full_name}\n"
             f"ID: {user.id}\n\n"
             f"Message:\n{message}\n\n"
             f"Reply using:\n/reply {user.id} your message"
    )

    await update.message.reply_text("Your message has been received ✅")

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

        await update.message.reply_text("Message sent ✅")

    except:
        await update.message.reply_text(
            "Use:\n/reply ID message"
        )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("reply", reply_user))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_message))

app.run_polling()
