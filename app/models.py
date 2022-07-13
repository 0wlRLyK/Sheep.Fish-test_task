from datetime import datetime
from textwrap import wrap

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now

from app.card import fields
from app.card.types import get_type_name
from app.model_data import CATEGORIES_VALUES, STATUS_ICONS


class Card(models.Model):
    class Statuses(models.IntegerChoices):
        UNACTIVE = 0
        ACTIVE = 1
        EXPIRED = 2

    number = fields.CardNumberField(unique=True)
    start_date = models.DateTimeField()
    expired_date = fields.CardExpiryField()
    code = fields.SecurityCodeField()
    value = models.DecimalField(decimal_places=2, max_digits=30)
    card_status = models.PositiveSmallIntegerField(choices=Statuses.choices)

    def __str__(self):
        return f"{self.number_formatted} - {self.expired_date}"

    @property
    def status(self):
        return STATUS_ICONS.get(self.card_status)

    @property
    def card_type(self):
        return get_type_name(self.number)

    @property
    def number_formatted(self):
        return " ".join(wrap(self.number, 4))

    def clean(self):
        if isinstance(self.expired_date, str):
            expired_date = datetime.strptime(self.expired_date, "%m/%y")
        else:
            expired_date = self.expired_date
        if self.start_date.date() > expired_date.date():
            raise ValidationError(
                {"start_date": "The date of issue of the card cannot be later than the date of expiry of its term"})

    def save(self, *args, **kwargs):
        self.clean()
        if isinstance(self.expired_date, str):
            expired_date = datetime.strptime(self.expired_date, "%m/%y")
        else:
            expired_date = self.expired_date
        if now().date() > expired_date.date():
            self.card_status = 2
        return super().save(*args, **kwargs)


class Activity(models.Model):
    class Categories(models.IntegerChoices):
        OTHER = 0
        PRODUCTS = 1
        AUTO = 2
        CHARITY = 3
        BUDGET = 4
        SHIPMENTS = 5
        CASH = 6
        TRANSFERS = 7
        STATIONERY = 8
        CAFE = 9
        FLOWERS = 10
        MOVIES = 11
        BOOKS = 12
        UTILITY = 13
        COURIER = 14
        MEDICINE = 15
        CLOTHES = 16
        STITCHING = 17
        ELECTRONICS = 18
        CREDIT = 19
        TRAVELS = 20
        PARTS = 21
        MOBILE = 22
        MARKETING = 23
        REPAIR = 24
        ENTERTAINMENT = 25
        TAXI = 26
        PETS = 27
        FINES = 28
        JEWERLY = 29
        DUTY_FREE = 30

    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    category = models.PositiveSmallIntegerField(choices=Categories.choices, default=0)
    name = models.CharField(max_length=250)
    value = models.DecimalField(decimal_places=2, max_digits=30)
    date = models.DateTimeField(default=now())

    class Meta:
        ordering = ('-date', )

    @property
    def category_data(self):
        return CATEGORIES_VALUES.get(self.category)


    @property
    def value_color(self):
        if self.value > 0:
            return "#5db361"
        elif 0 > self.value:
            return "#b35d5d"
        else:
            return "#5d96b3"