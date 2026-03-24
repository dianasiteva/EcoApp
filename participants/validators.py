from django.core.validators import RegexValidator

plate_validator = RegexValidator(
    regex=r'^[A-Z0-9]{4,8}$',
    message='Регистрационният номер трябва да съдържа само главни латински букви и цифри (4–8 символа).'
)