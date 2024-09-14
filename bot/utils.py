default_languages = {
    "uz": {
        'welcome_message': "Salom, botimizga xush kelibsiz",
        'choose_language': "Quyidagi tillardan birini tanlang",
        'individual': "Jismoniy shaxs",
        'legal': "Yuridik shaxs",
        'registration': "Ruyhatdan o'tish"
    },
    "ru": {
        "welcome_message": "Здравствуйте, добро пожаловать в наш бот",
        'choose_language': "Выберите один из языков ниже",
        'individual': "частное лицо",
        'legal': "юридическое лицо",
        'registration': 'Регистрация',

    }

}

introduction_template = (
    """
    💧Chere Water Company представляет @ChereBot 💧

    Решите все вопросы, связанные с водой Chere! 🚰

    Что может сделать бот?
    - Заказ воды
    - Знать о последних тарифах на воду
    - Проверка расчетов
    - Будьте в курсе эксклюзивных скидок и акций
    - Вопросы и помощь
    🌐 ChereBot - легкий и быстрый сервис!

    🏠 Оставайтесь дома и пользуйтесь уникальными услугами!

    🟢 Присоединяйтесь прямо сейчас: @ChereBot
    ✉️  Телеграм канал: @chereuz

    Chere - Чистая вода, Здоровая жизнь!

    """
)

def calculate_total_water(week_days, employee_count, durations_days):
    available_days = int(durations_days) // int(week_days) + int(durations_days) % int(week_days)
    return available_days * int(employee_count) * 2