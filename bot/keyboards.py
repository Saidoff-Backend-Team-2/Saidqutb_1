from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from bot.utils import default_languages


def get_languages():
    lang = InlineKeyboardMarkup()
    lang_uz = InlineKeyboardButton(text="uz 🇺🇿", callback_data="lang_uz")
    lang_ru = InlineKeyboardButton(text="ru 🇷🇺", callback_data="lang_ru")

    lang.add(lang_uz, lang_ru)
    return lang


def user_types(lang):
    person = InlineKeyboardMarkup()
    individual = InlineKeyboardButton(text=default_languages[lang]['individual'], callback_data="individual")
    legal = InlineKeyboardButton(text=default_languages[lang]["legal"], callback_data="legal")
    person.add(individual, legal)
    return person


def get_registration(lang):
    reg = InlineKeyboardMarkup()
    reg_btn = InlineKeyboardButton(text=default_languages[lang]['registration'], callback_data="registration")
    reg.add(reg_btn)
    return reg


def get_contact(lang):
    btn_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton(text="Kontaktni yuborish", request_contact=True)
    btn_markup.add(btn)
    return btn_markup


def get_main_menu(lang):
    main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
    web_app = KeyboardButton(text="📎 WebApp")
    settings = KeyboardButton(text="⚙️ Settings")
    contact_us = KeyboardButton(text="📲 Contact Us")
    my_orders = KeyboardButton(text="📦 My Orders")
    main_menu.add(web_app, settings, contact_us, my_orders)
    return main_menu