import aiosqlite
import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import nest_asyncio
import asyncio
from datetime import datetime, timedelta

nest_asyncio.apply()  # PyDroid/Railway uchun

# ===== TOKEN VA ADMIN =====
TOKEN = "8426295239:AAGun0-AbZjsUiEDH3wEShOEIBqFcFVVIWM"  # o'zingiz token qo'yasiz
ADMIN = 5775388579

# ===== MENYULAR =====
user_menu = ReplyKeyboardMarkup(
[
["🎬 Kino bot","📢 Obuna bot"],
["🤖 Avto javob","💬 Support bot"],
["📁 Botlarim"]
], resize_keyboard=True
)

admin_menu = ReplyKeyboardMarkup(
[
["📊 Statistika","👥 Users"],
["🤖 Barcha botlar"],
["💰 To‘lovlar"]
], resize_keyboard=True
)

state = {}

# ===== DATABASE INIT =====
async def init_db():
    async with aiosqlite.connect("safobuilder.db") as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            free_bots INTEGER DEFAULT 0,
            paid_balance INTEGER DEFAULT 0,
            last_free_date TEXT
        )
        """)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS bots(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner INTEGER,
            username TEXT,
            token TEXT,
            type TEXT,
            active_until TEXT,
            premium INTEGER DEFAULT 0,
            active INTEGER DEFAULT 1
        )
        """)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS payments(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            bot_id INTEGER,
            amount INTEGER,
            date TEXT
        )
        """)
        await db.commit()

# ===== START COMMAND =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    async with aiosqlite.connect("safobuilder.db") as db:
        await db.execute("INSERT OR IGNORE INTO users(id, free_bots, paid_balance, last_free_date) VALUES(?,?,?,?)",
                         (chat_id, 0, 0, datetime.now().strftime("%Y-%m-%d")))
        await db.commit()
    if chat_id == ADMIN:
        await update.message.reply_text("👑 ADMIN PANEL",reply_markup=admin_menu)
    else:
        await update.message.reply_text(
            "🚀 FULL PULLIK BOT MAKER\nBot turini tanlang:",
            reply_markup=user_menu
        )

# ===== MESSAGE HANDLER =====
async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    text = update.message.text

    # ----- BOT TANLASH -----
    if text in ["🎬 Kino bot","📢 Obuna bot","🤖 Avto javob","💬 Support bot"]:
        state[chat_id] = text
        await update.message.reply_text("BotFather token yuboring:")
        return

    # ----- TOKEN QABUL -----
    if chat_id in state:
        token_text = text
        url = f"https://api.telegram.org/bot{token_text}/getMe"
        r = requests.get(url)
        if r.status_code != 200 or not r.json()["ok"]:
            await update.message.reply_text("❌ Token xato!")
            return

        username = r.json()["result"]["username"]
        bot_type = state[chat_id]

        async with aiosqlite.connect("safobuilder.db") as db:
            # check free bot
            cursor = await db.execute("SELECT free_bots,last_free_date FROM users WHERE id=?", (chat_id,))
            row = await cursor.fetchone()
            free_bots = row[0]
            last_free_date = datetime.strptime(row[1], "%Y-%m-%d")

            today = datetime.now()

            if free_bots == 0:
                # 1 ta bepul bot
                active_until = (today + timedelta(days=7)).strftime("%Y-%m-%d")
                premium = 0
                await db.execute("UPDATE users SET free_bots=1,last_free_date=? WHERE id=?",
                                 (today.strftime("%Y-%m-%d"), chat_id))
                await update.message.reply_text("🎁 Sizning bepul botingiz 7 kun ishlaydi")
            else:
                # premium bot (pullik)
                active_until = (today + timedelta(days=30)).strftime("%Y-%m-%d")
                premium = 1
                await update.message.reply_text(
                    "💰 Premium bot yaratildi (1 oy davomida ishlaydi).\nPremium sotib olmoqchi bo‘lsangiz @Sardorbeko008 ga yozing."
                )

            await db.execute(
                "INSERT INTO bots(owner,username,token,type,active_until,premium,active) VALUES(?,?,?,?,?,?,?)",
                (chat_id,username,token_text,bot_type,active_until,premium,1)
            )
            await db.commit()

        await update.message.reply_text(f"✅ Bot qo‘shildi!\n@{username}", reply_markup=user_menu)
        await context.bot.send_message(
            ADMIN,
            f"🆕 Yangi bot!\nUser:{chat_id}\n@{username}\nType:{bot_type}"
        )
        state.pop(chat_id)
        return

    # ----- MY BOTS -----
    if text == "📁 Botlarim":
        async with aiosqlite.connect("safobuilder.db") as db:
            cursor = await db.execute("SELECT username,type,active_until,premium,active FROM bots WHERE owner=?",(chat_id,))
            bots = await cursor.fetchall()
        if not bots:
            await update.message.reply_text("Sizda bot yo‘q.")
            return
        msg = ""
        for b in bots:
            status = "✅" if b[4]==1 else "⏹"
            premium_text = "Premium" if b[3]==1 else "Bepul"
            msg += f"@{b[0]} → {b[1]} | {premium_text} | {status} | Muddati: {b[2]}\n"
        await update.message.reply_text(msg)

    # ----- ADMIN PANEL -----
    if chat_id == ADMIN:
        if text == "📊 Statistika":
            async with aiosqlite.connect("safobuilder.db") as db:
                u = await db.execute("SELECT COUNT(*) FROM users")
                users = (await u.fetchone())[0]
                b = await db.execute("SELECT COUNT(*) FROM bots")
                bots = (await b.fetchone())[0]
            await update.message.reply_text(f"👥 Users: {users}\n🤖 Bots: {bots}")

        if text == "👥 Users":
            async with aiosqlite.connect("safobuilder.db") as db:
                cursor = await db.execute("SELECT id FROM users")
                users = await cursor.fetchall()
            await update.message.reply_text("\n".join([str(u[0]) for u in users]))

        if text == "🤖 Barcha botlar":
            async with aiosqlite.connect("safobuilder.db") as db:
                cursor = await db.execute("SELECT username,type,active_until,premium,active FROM bots")
                bots = await cursor.fetchall()
            msg=""
            for b in bots:
                status = "✅" if b[4]==1 else "⏹"
                premium_text = "Premium" if b[3]==1 else "Bepul"
                msg += f"@{b[0]} → {b[1]} | {premium_text} | {status} | Muddati: {b[2]}\n"
            await update.message.reply_text(msg)

        if text == "💰 To‘lovlar":
            async with aiosqlite.connect("safobuilder.db") as db:
                cursor = await db.execute("SELECT user_id,bot_id,amount,date FROM payments")
                payments = await cursor.fetchall()
            if not payments:
                await update.message.reply_text("To‘lovlar yo‘q.")
                return
            msg=""
            for p in payments:
                msg += f"User:{p[0]} | Bot:{p[1]} | Summa:{p[2]} | Sana:{p[3]}\n"
            await update.message.reply_text(msg)

# ====== BOT CHECK (muddati tugagach) ======
async def check_bots():
    while True:
        today = datetime.now().strftime("%Y-%m-%d")
        async with aiosqlite.connect("safobuilder.db") as db:
            cursor = await db.execute("SELECT id,owner,username,active_until,premium,active FROM bots")
            bots = await cursor.fetchall()
            for b in bots:
                if b[5]==1 and b[4]==0 and datetime.strptime(b[3],"%Y-%m-%d") < datetime.now():
                    await db.execute("UPDATE bots SET active=0 WHERE id=?",(b[0],))
                    await db.commit()
                    try:
                        await app.bot.send_message(b[1],f"⏰ Sizning bepul botingiz @{b[2]} muddati tugadi! Premium sotib olmoqchi bo‘lsangiz @Sardorbeko008 ga yozing.")
                    except: pass
        await asyncio.sleep(3600)

# ===== MAIN =====
async def main():
    global app
    await init_db()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start",start))
    app.add_handler(MessageHandler(filters.TEXT,message))
    asyncio.create_task(check_bots())
    print("🔥 FULL SAFOBUILDER BOT PLATFORM ISHLADI!")
    await app.run_polling()

# ===== RUN =====
if __name__ == "__main__":
    asyncio.run(main())
