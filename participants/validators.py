from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

plate_validator = RegexValidator(
    regex=r'^[A-Z0-9]{4,8}$',
    message='Регистрационният номер трябва да съдържа само главни латински букви и цифри (4–8 символа).'
)


def validate_image(file):
    max_size_mb = 5
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"Снимката трябва да е под {max_size_mb}MB.")

    valid_extensions = ["jpg", "jpeg", "png"]
    ext = file.name.split(".")[-1].lower()
    if ext not in valid_extensions:
        raise ValidationError("Позволени формати: JPG, JPEG, PNG.")
