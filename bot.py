import json
import subprocess
import sys
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

MASTER_TOKEN = "8511690084:AAE5bCLOO3rXwsZQNJ3JjjSmNxL-4MMlG80"
MASTER_ADMIN = 5775388579
MENU = ReplyKeyboardMarkup(
    [["🎬 Kino bot yaratish"]],
    resize_keyboard=True
)

STATE = {}

# users.json yaratish
try:
    open("users.json", "r")
except:
    with open("users.json", "w") as f:
        json.dump({}, f)


# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat_id == MASTER_ADMIN:
        await update.message.reply_text(
            "🔥 MASTER BOT ishlayapti!",
            reply_markup=MENU
        )
    else:
        await update.message.reply_text(
            "Bot yaratish uchun tugmani bosing 👇",
            reply_markup=MENU
        )


# MESSAGE
async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.message.chat_id
    text = update.message.text

    if text == "🎬 Kino bot yaratish":
        STATE[chat_id] = "token"
        await update.message.reply_text(
            "BotFatherdan olgan TOKENni yuboring:"
        )
        return

    if STATE.get(chat_id) == "token":

        token = text.strip()

        # users.json ga yozamiz
        with open("users.json", "r") as f:
            users = json.load(f)

        users[str(chat_id)] = token

        with open("users.json", "w") as f:
            json.dump(users, f)

        # USER BOTNI ISHGA TUSHIRAMIZ
        subprocess.Popen(
            [sys.executable, "user_bot.py", token, str(chat_id)]
        )

        await update.message.reply_text(
            "✅ Bot yaratildi!\n\n"
            "Endi o‘z botingizga kirib /panel yozing."
        )

        STATE.pop(chat_id)


def main():
    app = ApplicationBuilder().token(MASTER_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, message))

    print("MASTER BOT ISHLADI 🔥")

    app.run_polling()


if __name__ == "__main__":
    main()
