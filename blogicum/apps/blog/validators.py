from datetime import datetime

from django.core.exceptions import ValidationError


def correct_date(value: datetime) -> None:
    today_date = datetime.today().date()

    if value.date() < today_date:
        raise ValidationError('Нельзя задать дату в прошлом!')
