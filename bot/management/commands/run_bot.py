from django.core.management.base import BaseCommand
from django.conf import settings

import telebot
from telebot.types import ReplyKeyboardRemove, ReplyKeyboardMarkup
from bot.keyboards import get_languages, user_types, get_registration, get_contact, get_main_menu, get_confirm_button
from bot.utils import default_languages, introduction_template, calculate_total_water
from bot.states import LegalRegisterState, IndividualRegisterState
from bot.crud import create_user, get_user_db

BOT_TOKEN = settings.BOT_TOKEN

bot = telebot.TeleBot(token=BOT_TOKEN)

user_languages = {}

all_languages = ['uz', 'ru']

@bot.message_handler(commands=['start'])
def welcome(message):
    lang_uz = default_languages['uz']
    lang_ru = default_languages['ru']
    text = (f"{lang_uz['welcome_message']}\n"
            f"{lang_uz['choose_language']}\n\n"
            f"{lang_ru['welcome_message']}\n"
            f"{lang_ru['choose_language']}\n")


    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=get_languages())
    bot.send_message(chat_id=message.chat.id, text="Tilni tanlang", reply_markup=ReplyKeyboardRemove())

@bot.callback_query_handler(func=lambda call: call.data == 'registration')
def registration(call):
    lang = user_languages[call.from_user.id]
    text = "Foydalanuvchi turini tanlang"
    bot.send_message(chat_id=call.from_user.id, text=text, reply_markup=user_types(lang))


@bot.callback_query_handler(func=lambda call: call.data.split("_")[0] == 'lang')
def select_language(call):

    user_id = call.from_user.id

    lang = call.data.split("_")[1]

    if lang in all_languages:
        user_languages[user_id] = call.data.split("_")[1]
        user = get_user_db(username=call.from_user.username)
        if user is not None:
            bot.send_message(chat_id=call.from_user.id, text=introduction_template,
                             reply_markup=get_main_menu(lang))
        else:
            bot.send_message(chat_id=call.from_user.id, text=introduction_template, reply_markup=get_registration(lang))
    else:
        bot.send_message(chat_id=user_id, text="You are not choose right language")




@bot.callback_query_handler(lambda call: call.data in ['legal', 'individual'])
def check_registration(call):
    if call.data == 'legal':
        bot.send_message(chat_id=call.from_user.id, text="Kompaniya nomini kiriting")
        bot.set_state(user_id=call.from_user.id, state=LegalRegisterState.COMPANY_NAME)
    elif call.data == 'individual':
        bot.send_message(chat_id=call.from_user.id, text="To'liq ismingizni kiriting")
        bot.set_state(user_id=call.from_user.id, state=IndividualRegisterState.NAME)



@bot.message_handler(func=lambda message: bot.get_state(message.from_user.id) == IndividualRegisterState.NAME)
def individual_name(message):

    lang = user_languages[message.from_user.id]
    data = {
        "full_name": message.text
    }

    bot.add_data(user_id=message.chat.id,  **data)
    bot.set_state(user_id=message.from_user.id, state=IndividualRegisterState.CONTACT)
    bot.send_message(chat_id=message.chat.id, text="Kontaktingizni kiriting", reply_markup=get_contact(lang))



@bot.message_handler(content_types=["contact"], func=lambda message: bot.get_state(message.from_user.id) == IndividualRegisterState.CONTACT)
def individual_contact(message):
    lang = user_languages[message.from_user.id]

    with bot.retrieve_data(user_id=message.chat.id) as data:
        data['phone_number'] = message.contact.phone_number

    bot.set_state(user_id=message.from_user.id, state=IndividualRegisterState.PASSWORD)
    bot.add_data(user_id=message.chat.id, **data)
    bot.send_message(chat_id=message.chat.id, text="Akkountingiz uchun parol kiriting")


@bot.message_handler(func = lambda message: bot.get_state(message.from_user.id) == IndividualRegisterState.PASSWORD)
def individual_password(message):
    lang = user_languages[message.from_user.id]
    with bot.retrieve_data(user_id=message.chat.id) as data:
        pass
    data['password'] = message.text
    data['telegram_id'] = message.from_user.id
    data['username'] = message.from_user.username

    user = create_user(data, 'individual')
    bot.send_message(chat_id=message.from_user.id, text="Siz muvaffaqqiyatli ro'yhatdan o'tdingiz", reply_markup=get_main_menu(lang))



@bot.message_handler(func=lambda message: bot.get_state(message.from_user.id) == LegalRegisterState.COMPANY_NAME)
def legal_company_name(message):
    lang = user_languages[message.from_user.id]
    data = {
        "company_name": message.text
    }
    bot.add_data(user_id=message.chat.id, **data)
    bot.set_state(user_id=message.chat.id, state=LegalRegisterState.EMPLOYEE_NAME)
    bot.send_message(chat_id=message.from_user.id, text="Xodim ismini kiriting")


@bot.message_handler(func=lambda message: bot.get_state(message.from_user.id) == LegalRegisterState.EMPLOYEE_NAME)
def legal_employee_name(message):
    lang = user_languages[message.from_user.id]
    with bot.retrieve_data(user_id=message.chat.id) as data:
        data['employee_name'] = message.text
    bot.add_data(user_id=message.chat.id, **data)

    bot.set_state(user_id=message.chat.id, state=LegalRegisterState.COMPANY_CONTACT)
    bot.send_message(chat_id=message.chat.id, text="Kontaktingizni kiriting", reply_markup=get_contact(lang))


@bot.message_handler(content_types=["contact"], func=lambda message: bot.get_state(message.from_user.id) == LegalRegisterState.COMPANY_CONTACT)
def legal_company_contact(message):
    lang = user_languages[message.from_user.id]
    with bot.retrieve_data(user_id=message.chat.id) as data:
        data['phone_number'] = message.contact.phone_number

    bot.set_state(user_id=message.chat.id, state=LegalRegisterState.EMPLOYEE_COUNT)
    bot.send_message(chat_id=message.chat.id, text="Xodimlar sonini kiriting")


@bot.message_handler(func=lambda message: bot.get_state(message.from_user.id) == LegalRegisterState.EMPLOYEE_COUNT)
def legal_employee_count(message):
    lang = user_languages[message.from_user.id]
    with bot.retrieve_data(user_id=message.chat.id) as data:
        data['employees_count'] = message.text

    bot.set_state(user_id=message.chat.id, state=LegalRegisterState.DURATION_DAYS)
    bot.add_data(user_id=message.chat.id, **data)
    bot.send_message(chat_id=message.chat.id, text="Suv yetkazib berish davomiyligini kiriting(kunda)")


@bot.message_handler(func=lambda message: bot.get_state(message.from_user.id) == LegalRegisterState.DURATION_DAYS)
def legal_duration(message):
    lang = user_languages[message.from_user.id]
    with bot.retrieve_data(user_id=message.chat.id) as data:
        data['duration_days'] = message.text

    bot.set_state(user_id=message.chat.id, state=LegalRegisterState.WORKING_DAYS)
    bot.send_message(chat_id=message.chat.id, text="Sizning ishxonangizda ish kunlari haftasiga nechi kun")


@bot.message_handler(func=lambda message: bot.get_state(message.from_user.id) == LegalRegisterState.WORKING_DAYS)
def legal_working_day(message):
    lang = user_languages[message.from_user.id]
    with bot.retrieve_data(user_id=message.chat.id) as data:
        data['working_days'] = message.text


    bot.set_state(user_id=message.chat.id, state=LegalRegisterState.PASSWORD)
    bot.add_data(user_id=message.chat.id, **data)
    bot.send_message(chat_id=message.chat.id, text="Akkountingiz uchun parol kiriting")


@bot.message_handler(func = lambda message: bot.get_state(message.from_user.id) == LegalRegisterState.PASSWORD)
def legal_password(message):
    lang = user_languages[message.from_user.id]
    with bot.retrieve_data(user_id=message.chat.id) as data:
        pass

    data['telegram_id'] = message.from_user.id
    data['username'] = message.from_user.username
    data['password'] = message.text

    duration_days = data['duration_days']
    del data['duration_days']
    total_water = calculate_total_water(data['working_days'], data['employees_count'], duration_days)
    text = (f"Xodim: {data['employees_count']}\n"
            f"Davomiylik kuni: {duration_days}\n"
            f"Sizning ishchilaringiz uchun  {int(total_water)//20} ta 20 l suv\n"
            )

    user = create_user(data, 'legal')
    bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=get_confirm_button(lang))

class Command(BaseCommand):

    def handle(self, *args, **options):
        bot.infinity_polling()