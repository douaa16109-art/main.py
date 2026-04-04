import telebot
import os
from flask import Flask
from threading import Thread

# --- إعدادات البوت ---
# التوكن الذي قدمتِيه ومُعرّف المعلمة المستخرج
API_TOKEN = '8716799001:AAE0teJRfBQk7TzMFwqZ4zCuGK7E5eSpPtg'
TEACHER_ID = 8104529547 

bot = telebot.TeleBot(API_TOKEN)
app = Flask('')

# --- نظام الويب لضمان بقاء البوت نشطاً (Keep Alive) ---
@app.route('/')
def home():
    return "البوت يعمل بنجاح وهو الآن مستعد لاستقبال الواجبات!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- أوامر البوت ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "🌹 أهلاً بكِ في بوت استلام الواجبات.\n\n"
        "يرجى إرسال صورة الواجب أو الملف هنا مباشرة.\n"
        "💡 ملاحظة: الحل سيصل للمعلمة بخصوصية تامة ولن يراه أحد غيرها.\n"
        "⚠️ يرجى كتابة اسمكِ الثلاثي مع المرفق."
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(content_types=['photo', 'document', 'text'])
def handle_homework(message):
    try:
        # إرسال رسالة تأكيد للطالبة فوراً
        bot.reply_to(message, "✅ تم استلام واجبكِ وإرساله للمراجعة. بالتوفيق!")
        
        # إعادة توجيه الرسالة (الواجب) إلى المعلمة مباشرة
        bot.forward_message(TEACHER_ID, message.chat.id, message.message_id)
        
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "❌ عذراً، حدث خطأ في الإرسال. تأكدي من جودة الإنترنت وحاولي مجدداً.")

# --- تشغيل البوت ---
if __name__ == "__main__":
    keep_alive()  # تشغيل خادم الويب الصغير في الخلفية
    print("البوت انطلق بنجاح...")
    bot.polling(none_stop=True)
