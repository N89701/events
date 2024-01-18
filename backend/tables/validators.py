import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def numeric_only(postcode):
    if postcode.isdigit() is False:
        raise ValidationError('Почтовый индекс должен содержать только цифры')


def validate_telephone_number(number):
    pattern = r'^\+\d{7,14}$'
    if not bool(re.match(pattern, number)):
        raise ValidationError(
            'Телефонный номер должен начинаться с +, содержать от 7 до 14 цифр'
        )
