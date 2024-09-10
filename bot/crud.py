from django.db import IntegrityError

from account.models import User
from bot.keyboards import user_types


def create_user(user_data, user_type):
    print(user_data)
    try:
        if user_type == User.UserType.INDIVIDUAL:
            new_user = User.objects.create(
                full_name=user_data['full_name'],
                phone_number=user_data['phone_number'],
                telegram_id=user_data['telegram_id'],
                username=user_data['username'],
            )
        else:
            new_user = User.objects.create(
                username=user_data['username'],
                phone_number=user_data['phone_number'],
                company_name=user_data['company_name'],
                employee_name=user_data['employee_name'],

            )
        new_user.user_type = user_type
        new_user.save()
        return new_user
    except IntegrityError:
        raise Exception('User already exists')