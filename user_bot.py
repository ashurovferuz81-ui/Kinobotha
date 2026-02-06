import sys
import aiosqlite
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

TOKEN = sys.argv[1]
ADMIN_ID = int(sys.argv[2])

DB = f"bot_{ADMIN_ID}.db"

state = {}
temp = {}

# DATABASE
async def init_db():
    async with aiosqlite.connect(DB) as db:

        await db.execute("""
        CREATE TABLE IF NOT EXISTS movies(
            code TEXT PRIMARY KEY,
            file_id TEXT
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY
        )
        """)

        await db.commit()


# USER SAVE
async def save_user(user_id):
    async with aiosqlite.connect(DB) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users VALUES(?)",
            (user_id,)
        )
        await db.commit()


# PANEL
async def panel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.chat_id != ADMIN_ID:
        return

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Kino yuklash", callback_data="add")],
        [InlineKeyboardButton("📊 Statistika", callback_data="stats")],
        [InlineKeyboardButton("📁 Kinolar", callback_data="list")],
        [InlineKeyboardButton("🗑 Kino o‘chirish", callback_data="delete")]
    ])

    await update.message.reply_text(
        "👑 ADMIN PANEL",
        reply_markup=keyboard
    )


# BUTTON HANDLER
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.message.chat_id != ADMIN_ID:
        return

    data = query.data

    if data == "add":
        state[ADMIN_ID] = "code"
        await query.message.reply_text("🎬 Kino kodini yuboring:")

    elif data == "stats":

        async with aiosqlite.connect(DB) as db:
            cur = await db.execute("SELECT COUNT(*) FROM users")
            users = (await cur.fetchone())[0]

            cur = await db.execute("SELECT COUNT(*) FROM movies")
            movies = (await cur.fetchone())[0]

        await query.message.reply_text(
            f"📊 STATISTIKA\n\n👥 Obunachilar: {users}\n🎬 Kinolar: {movies}"
        )

    elif data == "list":

        async with aiosqlite.connect(DB) as db:
            cur = await db.execute("SELECT code FROM movies")
            rows = await cur.fetchall()

        if not rows:
            await query.message.reply_text("Kino yo‘q.")
            return

        text = "\n".join([r[0] for r in rows])

        await query.message.reply_text(
            f"📁 Kinolar:\n\n{text}"
        )

    elif data == "delete":
        state[ADMIN_ID] = "delete"
        await query.message.reply_text(
            "O‘chirmoqchi bo‘lgan kino kodini yuboring:"
        )


# MESSAGE
async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.message.chat_id

    await save_user(chat_id)

    # ADMIN FUNKSIYALARI
    if chat_id == ADMIN_ID:

        if state.get(chat_id) == "code":
            temp[chat_id] = update.message.text
            state[chat_id] = "video"

            await update.message.reply_text(
                "🎥 Endi kinoni VIDEO qilib yuboring:"
            )
            return

        if state.get(chat_id) == "video":

            if not update.message.video:
                await update.message.reply_text("Faqat video yuboring!")
                return

            code = temp[chat_id]
            file_id = update.message.video.file_id

            async with aiosqlite.connect(DB) as db:
                await db.execute(
                    "INSERT INTO movies VALUES(?,?)",
                    (code, file_id)
                )
                await db.commit()

            await update.message.reply_text("✅ Kino saqlandi!")

            state.pop(chat_id)
            temp.pop(chat_id)
            return

        if state.get(chat_id) == "delete":

            code = update.message.text

            async with aiosqlite.connect(DB) as db:
                await db.execute(
                    "DELETE FROM movies WHERE code=?",
                    (code,)
                )
                await db.commit()

            await update.message.reply_text("🗑 Kino o‘chirildi!")

            state.pop(chat_id)
            return


    # FOYDALANUVCHI KINO OLISHI
    if update.message.text:

        code = update.message.text

        async with aiosqlite.connect(DB) as db:
            cur = await db.execute(
                "SELECT file_id FROM movies WHERE code=?",
                (code,)
            )
            row = await cur.fetchone()

        if row:
            await context.bot.send_video(chat_id, row[0])


async def main():

    await init_db()

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("panel", panel))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.ALL, message))

    print("USER BOT SUPER ADMIN PANEL BILAN ISHLADI 🔥")

    app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
