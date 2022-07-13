import datetime
import random

from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import now

from app.models import Card, Activity
import ccard
from faker import Faker

CARD_NUMBER_GENERATOR = {
    "visa": ccard.visa,
    "mastercard": ccard.mastercard,
    "discover": ccard.discover,
    "american_express": ccard.americanexpress,
}
CARD_EXPIRED = {
    "1_рік": now() + datetime.timedelta(days=365),
    "1_місяць": now() + datetime.timedelta(days=30),
    "6_місяців": now() + datetime.timedelta(days=180),
    "просрочена": now(),
}

class Command(BaseCommand):
    help = 'Generates credit cards'


    def add_arguments(self, parser):
        parser.add_argument('type', type=str)
        parser.add_argument('quantity', type=int)
        parser.add_argument('expired', type=str)

    def handle(self, *args, **options):

        fake = Faker("uk")
        for poll_id in range(options['quantity']):
            date = CARD_EXPIRED.get(options['expired'], '10/22')

            card = Card.objects.create(
                number=CARD_NUMBER_GENERATOR[options['type']](),
                start_date=now(),
                expired_date=date,
                code=str(random.randint(100, 9999)),
                value=random.randint(1, 999999),
                card_status=random.randint(0, 2)
            )
            Activity.objects.bulk_create([
                Activity(
                    card=card,
                    name=f"{fake.company()} - {fake.address()}",
                    value=fake.pydecimal(right_digits=2, left_digits=7),
                    category=random.randint(0, 31)
                ) for num in range(random.randint(1, 15))
            ])

        self.stdout.write(self.style.SUCCESS(f'Successfully generated {options["quantity"]} cards'))