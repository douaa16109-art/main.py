import telebot
from telebot import types
from datetime import datetime
from hijri_converter import Gregorian

TOKEN = '8649317582:AAFfr-jpQ5CUarItt6jWR3cOFLTSCBqX2Ms'
bot = telebot.TeleBot(TOKEN)

# قاموس لحفظ بيانات الطالبات (مؤقت حتى يتم ربطه بقاعدة بيانات)
# الهيكل: {chat_id: {"students": {name: status}}}
data = {}

def get_dates():
    now = datetime.now()
    hdate = Gregorian.fromdate(now.date()).to_hijri()
    return f"{now.strftime('%d %B %Y')} | {hdate.day}/{hdate.month}/{hdate.year} هـ"

def generate_text(chat_id):
    date_str = get_dates()
    students = data.get(chat_id, {}).get("students", {})
    
    student_list = ""
    if not students:
        student_list = "لا يوجد مسجلات بعد.."
    else:
        for name, status in students.items():
            student_list += f"🌹 {name} {'✅' if status == 'read' else '🎧'}\n"

    text = (
        f"🎀━━━━━━━━━━━━━━━━🎀\n"
        f"📅 {date_str}\n\n"
        f"🌸 قال رسول الله ﷺ: «اقرؤوا القرآن فإنه يأتي يوم القيامة شفيعاً لأصحابه»\n\n"
        f"📋 القائمة:\n{student_list}\n"
        f"🎀━━━━━━━━━━━━━━━━🎀"
    )
    return text

def main_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    # استخدام التشكيل الملون بالأيقونات لمحاكاة الألوان
    btn1 = types.InlineKeyboardButton("📝 سجل اسمي", callback_data="reg")
    btn2 = types.InlineKeyboardButton("❌ حذف اسمي", callback_data="del")
    btn3 = types.InlineKeyboardButton("✅ قرأت", callback_data="read")
    btn4 = types.InlineKeyboardButton("🔒 إغلاق القائمة", callback_data="close")
    markup.add(btn1, btn2, btn3, btn4)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    if chat_id not in data:
        data[chat_id] = {"students": {}}
    bot.send_message(chat_id, generate_text(chat_id), reply_markup=main_markup())

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    user_name = call.from_user.first_name
    
    if call.data == "reg":
        data[chat_id]["students"][user_name] = "waiting"
    elif call.data == "read":
        data[chat_id]["students"][user_name] = "read"
    elif call.data == "del":
        if user_name in data[chat_id]["students"]:
            del data[chat_id]["students"][user_name]
            
    bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, 
                          text=generate_text(chat_id), reply_markup=main_markup())

bot.polling(none_stop=True)
