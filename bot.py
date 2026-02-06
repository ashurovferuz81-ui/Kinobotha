import asyncio
import aiosqlite
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

MASTER_TOKEN = "MASTER_BOT_TOKENINGIZNI_QUYING"
OWNER_ID = 5775388579
DB = "bots.db"


###################################
# DATABASE
###################################

async def init_db():
    async with aiosqlite.connect(DB) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER,
            bot_token TEXT
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            bot_token TEXT,
            code TEXT,
            file_id TEXT
        )
        """)

        await db.commit()


###################################
# USER BOT (kino bot)
###################################

async def run_user_bot(token, owner_id):

    app = ApplicationBuilder().token(token).build()

    keyboard = ReplyKeyboardMarkup(
        [["🎬 Kino yuklash", "📊 Statistika"]],
        resize_keyboard=True
    )

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id == owner_id:
            await update.message.reply_text(
                "✅ Admin panelga xush kelibsiz!",
                reply_markup=keyboard
            )
        else:
            await update.message.reply_text(
                "🎬 Kino kodini yuboring..."
            )

    async def panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id == owner_id:
            await update.message.reply_text(
                "🎛 Admin panel",
                reply_markup=keyboard
            )

    async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

        user_id = update.effective_user.id
        text = update.message.text

        # ADMIN KINO YUKLASH
        if user_id == owner_id:

            if text == "🎬 Kino yuklash":
                context.user_data["step"] = "code"
                await update.message.reply_text("Kino kodini yuboring:")
                return

            if context.user_data.get("step") == "code":
                context.user_data["movie_code"] = text
                context.user_data["step"] = "video"
                await update.message.reply_text("Endi kinoni VIDEO qilib yuboring:")
                return

        # VIDEO QABUL
        if update.message.video and user_id == owner_id:

            code = context.user_data.get("movie_code")

            if not code:
                return

            file_id = update.message.video.file_id

            async with aiosqlite.connect(DB) as db:
                await db.execute(
                    "INSERT INTO movies VALUES (?, ?, ?)",
                    (token, code, file_id)
                )
                await db.commit()

            context.user_data.clear()

            await update.message.reply_text("✅ Kino saqlandi!")
            return

        # FOYDALANUVCHI KINO OLSIN
        if text:

            async with aiosqlite.connect(DB) as db:
                cursor = await db.execute(
                    "SELECT file_id FROM movies WHERE bot_token=? AND code=?",
                    (token, text)
                )
                movie = await cursor.fetchone()

            if movie:
                await update.message.reply_video(movie[0])
            else:
                await update.message.reply_text("❌ Kino topilmadi")

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("panel", panel))
    app.add_handler(MessageHandler(filters.ALL, message))

    print("USER BOT ISHLADI:", token)

    await app.initialize()
    await app.start()
    await app.updater.start_polling()


###################################
# MASTER BOT
###################################

async def start_master(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot yaratish uchun token yuboring."
    )


async def create_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):

    token = update.message.text
    user_id = update.effective_user.id

    try:
        app_test = ApplicationBuilder().token(token).build()
        await app_test.initialize()
        await app_test.shutdown()
    except:
        await update.message.reply_text("❌ Token noto‘g‘ri!")
        return

    async with aiosqlite.connect(DB) as db:
        await db.execute(
            "INSERT INTO users VALUES (?, ?)",
            (user_id, token)
        )
        await db.commit()

    asyncio.create_task(run_user_bot(token, user_id))

    await update.message.reply_text(
        "✅ Bot ishga tushdi!\n\nBotingizga kirib /start bosing."
    )


###################################
# LOAD BOTS (restartdan keyin ham ishlaydi)
###################################

async def load_bots():
    async with aiosqlite.connect(DB) as db:
        cursor = await db.execute("SELECT user_id, bot_token FROM users")
        bots = await cursor.fetchall()

    for user_id, token in bots:
        asyncio.create_task(run_user_bot(token, user_id))


###################################
# MAIN
###################################

async def main():

    await init_db()

    master = ApplicationBuilder().token(MASTER_TOKEN).build()

    master.add_handler(CommandHandler("start", start_master))
    master.add_handler(MessageHandler(filters.TEXT, create_bot))

    await master.initialize()
    await master.start()
    await master.updater.start_polling()

    await load_bots()

    print("🔥 MASTER BOT ISHLADI")

    while True:
        await asyncio.sleep(999999)


asyncio.run(main())
