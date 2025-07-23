import telebot
import requests
import os
from dotenv import load_dotenv

# تحميل المتغيرات من ملف .env
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def ask_openai(message):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": message}]
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"❌ خطأ من OpenAI: {response.status_code}\n{response.text}"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_msg = (
        "🤖 *مرحباً بك في بوت الذكاء الاصطناعي!*\n\n"
        "أنا نموذج محادثة مبني على تقنية *ChatGPT* من شركة *OpenAI*.\n"
        "تم تطوير هذا البوت بواسطة: _عبدالرحمن جمال عبدالرب العطاس_.\n\n"
        "💬 أرسل أي رسالة وسأرد عليك بذكاء."
    )
    bot.send_message(message.chat.id, welcome_msg, parse_mode='Markdown')

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_msg = message.text
    bot.send_chat_action(message.chat.id, 'typing')
    reply = ask_openai(user_msg)
    bot.reply_to(message, reply)

print("✅ Bot is running...")
bot.polling()
