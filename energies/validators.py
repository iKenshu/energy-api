import datetime

from rest_framework.validators import  ValidationError

def validate_date(date):
    if date is not None:
        try:
            datetime.date.fromisoformat(date)
        except ValueError:
            raise ValidationError(
                "Apparently you use an incorret date format. Please try again with 'YYYY-MM-DD'"
            )

def validate_period(period):
    if period not in ["daily", "weekly", "monthly"] and period != None:
        raise ValidationError(
            "That is not a valid argument. Please try 'daily', 'weekly' or 'monthly'"
        )
