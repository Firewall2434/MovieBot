from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    API_ID = int(os.environ.get("API_ID"))
    API_HASH = os.environ.get("API_HASH")
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    VERIFY_CHANNEL = os.environ.get("VERIFY_CHANNEL")
    MAIN_CHANNEL_LINK = os.environ.get("MAIN_CHANNEL_LINK")

    for key, value in {
        "API_ID": API_ID,
        "API_HASH": API_HASH,
        "BOT_TOKEN": BOT_TOKEN,
        "VERIFY_CHANNEL": VERIFY_CHANNEL,
        "MAIN_CHANNEL_LINK": MAIN_CHANNEL_LINK
    }.items():
        if not value:
            raise ValueError(f"Missing env variable: {key}")

except Exception as e:
    logger.error(f"Environment variable error: {e}")
    exit("❌ Bot stopped due to missing configuration.")

app = Client("verify_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def is_verified(status):
    return status in ["member", "administrator", "creator"]

@app.on_message(filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id
    logger.info(f"/start from {user_id}")

    try:
        member = await client.get_chat_member(VERIFY_CHANNEL, user_id)

        if is_verified(member.status):
            await message.reply_text(
                "✅ You are verified!
Here’s your access to the movie channel:",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("🎬 Join Movie Channel", url=MAIN_CHANNEL_LINK)]]
                )
            )
        else:
            raise ValueError("User not verified")

    except Exception as e:
        logger.warning(f"Verification failed for {user_id}: {e}")
        await message.reply_text(
            "❗ To access the movie channel, you must first join our verification channel.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("🔗 Join Verification Channel", url=f"https://t.me/{VERIFY_CHANNEL}")],
                    [InlineKeyboardButton("✅ I’ve Joined", callback_data="check_join")]
                ]
            )
        )

@app.on_callback_query(filters.regex("check_join"))
async def check_join(client, callback_query):
    user_id = callback_query.from_user.id
    logger.info(f"Check join from {user_id}")

    try:
        member = await client.get_chat_member(VERIFY_CHANNEL, user_id)

        if is_verified(member.status):
            await callback_query.message.edit_text(
                "✅ Verified again!
Here’s the movie channel access:",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("🎬 Join Movie Channel", url=MAIN_CHANNEL_LINK)]]
                )
            )
        else:
            raise ValueError("Still not a verified member")

    except Exception as e:
        logger.warning(f"Join check failed for {user_id}: {e}")
        await callback_query.answer("❌ You're still not a member. Please join the channel first.", show_alert=True)

if __name__ == "__main__":
    logger.info("Bot is starting...")
    app.run()