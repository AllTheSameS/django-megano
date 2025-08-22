from django.core.validators import RegexValidator


def phone_validator():
    return RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Номер должен быть в формате: '+999999999'",
        )