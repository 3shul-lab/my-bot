import telebot
import threading
import time
from flask import Flask

# සර්වර් එක 24 පැයම දුවන්න හදන කොටස
app = Flask('')

@app.route('/')
def home():
    return "Bot is successfully running 24/7!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# ඔයාගේ බොට්ගේ විස්තර
TOKEN = '8977132449:AAG-rekV5tDa1PnKKtyCKc-qPGdOeb-hHWg'
BOT_USERNAME = 'Ass_world_bot'
ACTUAL_CHANNEL_ID = -1003895697553

bot = telebot.TeleBot(TOKEN)

@bot.channel_post_handler(content_types=['text', 'photo', 'video', 'document', 'audio'], func=lambda message: True)
def generate_link(message):
    global ACTUAL_CHANNEL_ID
    ACTUAL_CHANNEL_ID = message.chat.id
    
    if message.video or message.document or message.photo:
        msg_id = message.message_id
        link = f"https://t.me/{BOT_USERNAME}?start=vid_{msg_id}"
        bot.send_message(message.chat.id, f"✅ ලින්ක් එක සාර්ථකයි!\n\nඔයාගේ ලින්ක් එක:\n{link}")

@bot.message_handler(commands=['start'])
def send_video(message):
    text = message.text.split()
    if len(text) > 1 and text[1].startswith('vid_'):
        try:
            vid_id = int(text[1].replace('vid_', ''))
            
            # කවුරුත් වීඩියෝ එක ඩවුන්ලෝඩ්/ෆෝවර්ඩ් කරන්නේ නැති වෙන්න හැදුවා
            bot.copy_message(message.chat.id, ACTUAL_CHANNEL_ID, vid_id, protect_content=True)
            
        except Exception:
            bot.reply_to(message, "❌ සමාවෙන්න, මේ වීඩියෝ එක හොයාගන්න බැරි වුණා.")
    else:
        bot.reply_to(message, "හායි! වීඩියෝ බලන්න අදාළ ලින්ක් එකෙන්ම එන්න ඕනේ.")

def bot_polling():
    while True:
        try:
            bot.polling(none_stop=True, timeout=20, long_polling_timeout=15)
        except Exception:
            time.sleep(5)

if __name__ == "__main__":
    t = threading.Thread(target=run_flask)
    t.start()
    bot_polling()
