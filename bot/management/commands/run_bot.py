from django.core.management.base import BaseCommand
from django.conf import settings

import telebot
from bot.keyboards import get_languages, user_types, get_registration, get_contact, get_main_menu
from bot.utils import default_languages, introduction_template
from bot.states import LegalRegisterState, IndividualRegisterState
from bot.crud import create_user

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
    print(message.contact.phone_number)
    with bot.retrieve_data(user_id=message.chat.id) as data:
        pass
    data['phone_number'] = message.contact.phone_number
    data['telegram_id'] = message.from_user.id
    data['username'] = message.from_user.username

    user = create_user(data, 'individual')
    bot.send_message(chat_id=message.from_user.id, text="Siz muvaffaqqiyatli ro'yhatdan o'tdingiz", reply_markup=get_main_menu(lang))



@bot.message_handler(func=lambda message: bot.get_state(message.from_user.id) == LegalRegisterState.COMPANY_NAME)
def legal_company_name(message):
    lang = user_languages[message.from_user.id]
    data = {
        "company_name": message
    }
    bot.add_data(user_id=message.chat.id, **data)
    bot.set_state(user_id=message.chat.id, state=LegalRegisterState.EMPLOYEE_NAME)
    bot.send_message(chat_id=message.from_user.id, text="Xodim ismini kiriting")


@bot.message_handler(func=lambda message: bot.get_state(message.from_user.id) == LegalRegisterState.EMPLOYEE_NAME)
def legal_employee_name(message):
    lang = user_languages[message.from_user.id]
    with bot.retrieve_data(user_id=message.chat.id) as data:
        data['employee_name'] = message
    bot.add_data(user_id=message.chat.id, **data)

    bot.set_state(user_id=message.chat.id, state=LegalRegisterState.COMPANY_CONTACT)
    bot.send_message(chat_id=message.chat.id, text="Kontaktingizni kiriting", reply_markup=get_contact(lang))


@bot.message_handler(func=lambda message: bot.get_state(message.from_user.id) == LegalRegisterState.COMPANY_CONTACT)
def legal_company_contact(message):
    lang = user_languages[message.from_user.id]
    with bot.retrieve_data(user_id=message.chat.id) as data:
        data['phone_number'] = message

    bot.set_state(user_id=message.chat.id, state=LegalRegisterState.EMPLOYEE_COUNT)
    bot.send_message(chat_id=message.chat.id, text="Xodimlar sonini kiriting")


@bot.message_handler(func=lambda message: bot.get_state(message.from_user.id) == LegalRegisterState.DURATION_DAYS)
def legal_duration(message):
    lang = user_languages[message.from_user.id]
    with bot.retrieve_data(user_id=message.chat.id) as data:
        data['duration_days'] = message

    bot.set_state(user_id=message.chat.id, state=LegalRegisterState.WORKING_DAYS)
    bot.send_message(chat_id=message.chat.id, text="Qancha vaqt mobaynida yetkazib berib turishimizni hohlaysiz")


@bot.message_handler(func=lambda message: bot.get_state(message.from_user.id) == LegalRegisterState.WORKING_DAYS)
def legal_working_day(message):
    lang = user_languages[message.from_user.id]
    with bot.retrieve_data(user_id=message.chat.id) as data:
        data['working_days'] = message
        data['telegram_id'] = message.from_user.id
        data['username'] = message.from_user.username
    duration_days = data['duration_days']
    del data['duration_days']

    user = create_user(data, 'legal')
    bot.send_message(chat_id=message.from_user.id, text="Ro'yhatdan o'tdingiz.")


class Command(BaseCommand):

    def handle(self, *args, **options):
        bot.infinity_polling()