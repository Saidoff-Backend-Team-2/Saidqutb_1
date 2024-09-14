from django.db import IntegrityError
import logging
from account.models import User, TelegramUser
from bot.keyboards import user_types

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def create_user(user_data, user_type):
    try:
        if TelegramUser.objects.filter(telegram_id=user_data['telegram_id']).exists():
            raise Exception('TelegramUser with this ID already exists')

        if user_type == User.UserType.INDIVIDUAL:
            new_user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'full_name': user_data['full_name'],
                    'phone_number': user_data['phone_number'],
                }
            )
        else:
            new_user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'phone_number': user_data['phone_number'],
                    'company_name': user_data['company_name'],
                    'full_name': user_data['employee_name'],
                }
            )

        if created:
            TelegramUser.objects.create(
                user=new_user,
                telegram_id=user_data['telegram_id'],
                telegram_username=user_data['username'],
            )

            new_user.user_type = user_type
            new_user.set_password(user_data['password'])
            new_user.save()

        return new_user

    except IntegrityError as e:
        logger.error(f"IntegrityError occurred: {e}. User data: {user_data}")
        raise Exception('User or TelegramUser already exists')


def get_user_db(username):
    user = TelegramUser.objects.filter(telegram_user=username).first()
    return user