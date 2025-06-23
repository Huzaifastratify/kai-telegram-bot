from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Load/Save Notes
def load_data():
    try:
        with open('data.json') as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f)

# /kai intro
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hey Huzaifa, I’m Kai — your AI co-founder. Let’s dominate together 💼🤖")

# /store command
async def store(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    if len(context.args) < 2:
        await update.message.reply_text("Use like this: /store [tag] [your note]")
        return
    tag = context.args[0]
    note = ' '.join(context.args[1:])
    data.setdefault(tag, []).append(note)
    save_data(data)
    await update.message.reply_text(f"✅ Stored under '{tag}': {note}")

# /fetch command
async def fetch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    tag = context.args[0] if context.args else None
    if tag is None:
        await update.message.reply_text("Use like this: /fetch [tag]")
        return
    notes = data.get(tag, [])
    if notes:
        await update.message.reply_text(f"🗂 Notes under '{tag}':\n" + '\n'.join(notes))
    else:
        await update.message.reply_text(f"No notes found under '{tag}'.")

# Setup App
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("kai", start))
    app.add_handler(CommandHandler("store", store))
    app.add_handler(CommandHandler("fetch", fetch))
    print("🤖 Kai is alive...")
    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
