import telebot
from telebot import types
from flask import Flask
from threading import Thread

# --- إعدادات البوت ---
API_TOKEN = '8716799001:AAE0teJRfBQk7TzMFwqZ4zCuGK7E5eSpPtg'
MY_ID = 7322325980  # الـ ID الخاص بكِ (أم عائشة)

# قائمة المعلمات (الأسماء تظهر مع الوردة في البوت)
TEACHERS = {
    "🌷 الْمُعَلِّمَةُ فَوْزِيَّة": 8104529547,
    "🌷 الْمُعَلِّمَةُ سَنَاء": 6266125898,
    "🌷 الْمُعَلِّمَةُ أَنِيسَة": 6018090830,
    "🌷 الْمُعَلِّمَةُ نَادِيَة": 1170097482
}

user_selections = {}
bot = telebot.TeleBot(API_TOKEN)
app = Flask('')

@app.route('/')
def home(): return "البوت يعمل بجمالية ونظام!"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # إنشاء لوحة الأزرار
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    
    # إضافة أسماء المعلمات مع الوردة
    for name in TEACHERS.keys():
        markup.add(types.KeyboardButton(name))
    
    # إضافة زر التجربة لَكِ أَنْتِ فَقَطْ (بشكل مميز)
    if message.chat.id == MY_ID:
        markup.add(types.KeyboardButton("✨ تَجْرِبَةُ الْبُوتِ (أَنَا)"))
    
    welcome_text = "السَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللهِ وَبَرَكَاتُهُ.\nلِمَنْ تُرِيدِينَ إِرْسَالَ حَلِّ الْوَاجِبِ يَا غَالِيَتِي؟"
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in TEACHERS.keys() or message.text == "✨ تَجْرِبَةُ الْبُوتِ (أَنَا)")
def set_teacher(message):
    if message.text == "✨ تَجْرِبَةُ الْبُوتِ (أَنَا)":
        user_selections[message.chat.id] = MY_ID
    else:
        user_selections[message.chat.id] = TEACHERS[message.text]
        
    instructions = (
        f"حَسَنًا، سَيَتِمُّ إِرْسَالُ حَلِّكِ إِلَى **{message.text}**.\n\n"
        "يُرْجَى الْآنَ إِرْسَالَ اسْمُكِ مَعَ حَلِّ الْوَاجِبِ (صُورَة، مَلَفّ، أَوْ نَصّ)."
    )
    bot.send_message(message.chat.id, instructions, parse_mode="Markdown")

@bot.message_handler(content_types=['photo', 'document', 'text', 'video', 'voice', 'audio'])
def forward_to_teacher(message):
    if message.chat.id in user_selections:
        target_id = user_selections[message.chat.id]
        try:
            bot.forward_message(target_id, message.chat.id, message.message_id)
            bot.reply_to(message, "✅ تَمَّ إِرْسَالُ هَذَا الْجُزْءِ بِنَجَاحٍ.")
        except Exception:
            bot.reply_to(message, "⚠️ الْمُعَلِّمَةُ لَمْ تُفَعِّلِ الْبُوتَ بَعْدُ.")
    else:
        bot.reply_to(message, "⚠️ يُرْجَى اخْتِيَارُ اسْمِ الْمُعَلِّمَةِ أَوَّلاً عبر /start")

def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

if __name__ == "__main__":
    keep_alive()
    bot.polling(none_stop=True)
