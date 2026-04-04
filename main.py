import telebot
from telebot import types
from flask import Flask
from threading import Thread

# --- إعدادات البوت الأساسية ---
# التوكن الخاص بكِ الذي زودتِني به
API_TOKEN = '8716799001:AAE0teJRfBQk7TzMFwqZ4zCuGK7E5eSpPtg'

# قاعدة البيانات النهائية بالأسماء والمعرفات المستخرجة
TEACHERS = {
    "الْمُعَلِّمَةُ فَوْزِيَّة": 8104529547,
    "الْمُعَلِّمَةُ سَنَاء": 6266125898,
    "الْمُعَلِّمَةُ أَنِيسَة": 6018090830,
    "الْمُعَلِّمَةُ نَادِيَة": 1170097482,
    "أُمُّ عَائِشَةَ (لِلتَّجْرِبَة)": 7322325980
}

# قاموس لتخزين وجهة الإرسال لكل طالبة بشكل مؤقت
user_selections = {}

bot = telebot.TeleBot(API_TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "البوت يعمل بنجاح ومستعد لاستقبال الواجبات!"

# --- أمر البداية /start ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # إنشاء أزرار الأسماء
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for name in TEACHERS.keys():
        markup.add(types.KeyboardButton(name))
    
    welcome_text = (
        "السَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللهِ وَبَرَكَاتُهُ.\n\n"
        "لِمَنْ تُرِيدِينَ إِرْسَالَ حَلِّ الْوَاجِبِ يَا غَالِيَتِي؟\n"
        "💡 اخْتَارِي اسْمَ الْمُعَلِّمَةِ مِنَ الْأَزْرَارِ أَدْنَاهُ."
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

# --- استقبال اختيار المعلمة وتثبيته ---
@bot.message_handler(func=lambda message: message.text in TEACHERS.keys())
def set_teacher(message):
    user_selections[message.chat.id] = TEACHERS[message.text]
    instructions = (
        f"حَسَنًا، سَيَتِمُّ إِرْسَالُ حَلِّكِ إِلَى **{message.text}**.\n\n"
        "يُرْجَى الْآنَ إِرْسَالَ اسْمُكِ الثُّلَاثِي مَعَ حَلِّ الْوَاجِبِ (صُورَة، مَلَفّ، أَوْ نَصّ).\n"
        "💡 كُلُّ مَا تُرْسِلِينَهُ الْآنَ سَيَصِلُ لِلْمُعَلِّمَةِ بِمُفْرَدِهَا بِنَجَاحٍ."
    )
    bot.send_message(message.chat.id, instructions, parse_mode="Markdown")

# --- تحويل الوسائط (صور، ملفات، فيديوهات، بصمات صوت، نصوص) ---
@bot.message_handler(content_types=['photo', 'document', 'text', 'video', 'voice', 'audio'])
def forward_to_teacher(message):
    # التأكد أن الطالبة اختارت معلمة أولاً
    if message.chat.id in user_selections:
        target_id = user_selections[message.chat.id]
        try:
            # توجيه الرسالة فوراً للمعلمة المختارة
            bot.forward_message(target_id, message.chat.id, message.message_id)
            bot.reply_to(message, "✅ تَمَّ إِرْسَالُ هَذِهِ الْمَادَّةِ إِلَى الْمُعَلِّمَةِ بِنَجَاحٍ.")
        except Exception as e:
            # في حال لم تضغط المعلمة على Start في البوت
            bot.reply_to(message, "⚠️ عُذْرًا، الْمُعَلِّمَةُ لَمْ تُفَعِّلِ الْبُوتَ بَعْدُ لاستقبال الرسائل.")
            print(f"Forward Error: {e}")
    else:
        # إذا أرسلت الطالبة شيئاً قبل اختيار الاسم
        bot.reply_to(message, "⚠️ يُرْجَى اخْتِيَارُ اسْمِ الْمُعَلِّمَةِ أَوَّلاً عبر الضغط على /start")

# --- تشغيل الخادم الصغير للبقاء نشطاً على الاستضافة ---
def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

if __name__ == "__main__":
    keep_alive()
    print("البوت انطلق بنجاح...")
    bot.polling(none_stop=True)
