# Telegram Verify Bot (Zeabur Ready)

A Telegram bot that verifies if a user has joined a specific channel before giving access to another one.

### Features
- Simple `/start` verification
- Detects member, admin, creator
- Retry option with button
- Fully deployable on Zeabur for free

### Setup Instructions
1. **Clone the repository**
2. **Create a `.env` file from `.env.example` and fill in your secrets**
3. **Push to GitHub**
4. **Go to [Zeabur](https://zeabur.com)** and deploy this repo
5. **Set your environment variables in the Zeabur UI** (same as in `.env`)

### Required ENV Vars
- `API_ID` and `API_HASH` — from [my.telegram.org](https://my.telegram.org)
- `BOT_TOKEN` — from [@BotFather](https://t.me/BotFather)
- `VERIFY_CHANNEL` — public channel username (no @)
- `MAIN_CHANNEL_LINK` — private channel invite link

---