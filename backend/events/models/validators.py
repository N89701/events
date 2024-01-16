from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def numeric_only(postcode):
    if postcode.isdigit() is False:
        raise ValidationError('Почтовый индекс должен содержать только цифры')


phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Телефонный номер должен быть формата: '+79265555555'"
    )
