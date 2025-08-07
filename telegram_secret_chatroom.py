import random
import os
import string
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
TOKEN=os.getenv(8349439002:AAHn-QPXNc4R90KV9MaPlGzwkNRQGYx1GbI)
print(f"TOKEN: {TOKEN}") 

nicknames = {}
rooms = {}      
user_room = {} 



def generate_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in nicknames:
        await update.message.reply_text(
            "Welcome to Secret Chat Bot By SDN 🤫\nPlease send me your nickname to continue."
        )
        nicknames[user_id] = None
    else:
        await update.message.reply_text(
            f"Welcome back {nicknames[user_id]}! 😎\nUse /create to start a secret chat or /join <code> to join one."
        )


async def set_nickname(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id in nicknames and nicknames[user_id] is None:
        nickname = update.message.text.strip()
        nicknames[user_id] = nickname
        await update.message.reply_text(
            f"Nice to meet you, {nickname}! 🎉\nUse /create to start a secret chat or /join <code> to join one."
        )
    else:
        if user_id in user_room:
            code = user_room[user_id]
            room = rooms.get(code)
            if room:
                for uid, uname in room["users"].items():
                    if uid != user_id:
                        await context.bot.send_message(uid, f"{nicknames[user_id]}: {update.message.text}")
        else:
            await update.message.reply_text("You already have a nickname! Use /create or /join to start chatting.")


async def create_room(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in nicknames or nicknames[user_id] is None:
        await update.message.reply_text("Please set a nickname first by sending a message.")
        return

    if user_id in user_room:
        await update.message.reply_text("You are already in a secret room! Use /clear to leave first.")
        return

    code = generate_code()
    rooms[code] = {"users": {user_id: nicknames[user_id]}}
    user_room[user_id] = code

    await update.message.reply_text(
        f"✅ Secret room created!\nShare this code with your friend: {code}\n"
        f"Or send this link: https://t.me/{context.bot.username}?start={code}\n"
        "They can join using /join <code>"
    )


async def join_room(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in nicknames or nicknames[user_id] is None:
        await update.message.reply_text("Please set a nickname first by sending a message.")
        return

    if user_id in user_room:
        await update.message.reply_text("You are already in a secret room! Use /clear to leave first.")
        return

    if len(context.args) != 1:
        await update.message.reply_text("Usage: /join <code>")
        return

    code = context.args[0].strip().upper()
    if code not in rooms:
        await update.message.reply_text("❌ Invalid or expired room code. Thanks for Using my Bot from SDN")
        return

    rooms[code]["users"][user_id] = nicknames[user_id]
    user_room[user_id] = code

    for uid in rooms[code]["users"]:
        await context.bot.send_message(uid, f"🎉 {nicknames[user_id]} has joined the secret chat!")


async def clear_session(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in user_room:
        await update.message.reply_text("You are not in any secret room.")
        return

    code = user_room[user_id]
    if code in rooms:
        for uid in list(rooms[code]["users"].keys()):
            await context.bot.send_message(uid, "❌ Secret chat cleared by a user. Session ended.\n Thank you From Sdn To using my Bot ")
            user_room.pop(uid, None)
        rooms.pop(code, None)


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("create", create_room))
    app.add_handler(CommandHandler("join", join_room))
    app.add_handler(CommandHandler("clear", clear_session))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, set_nickname))

    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
