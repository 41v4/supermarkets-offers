import logging
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from offers.models import Category, Notificator, Supermarket, Offer

logger = logging.getLogger('offer')

class Command(BaseCommand):
    help = 'Populate the Offer table with dummy data'

    def handle(self, *args, **options):
        offers = [
            {
                'product_name': 'Malta kava JACOBS KRONUNG, 500 g',
                'product_brand': 'JACOBS KRONUNG',
                'product_descr': 'Tik 05.02 - 05.08',
                'product_price': 4.59,
                'product_discount': None,
                'product_weight': None,
                'product_addt_info': 'Dviguboje kainodaroje nurodyta mažesnė įprasta kaina ir (ar) nuolaida taikoma su AČIŪ kortele. 1 kg – 9,18 €; be AČIŪ – 16,98 €',
                'product_img_orig': 'https://dummyimage.com/400x400',
                'product_img_local': 'https://dummyimage.com/400x400',
                'is_active': True,
                'valid_from': datetime.now(),
                'valid_until': datetime.now() + timedelta(days=7),
                'created_method': Offer.MAN,
                'updated_method': Offer.MAN,
                'deactivated_method': Offer.MAN,
                'category': Category.objects.get(id='5'),
                'supermarket': Supermarket.objects.get(name='maxima'),
                'abst_product': None,
            },
            {
                'product_name': 'Lietuviškiems obuoliams',
                'product_brand': None,
                'product_descr': 'Tik 05.02 - 05.08',
                'product_price': None,
                'product_discount': 30,
                'product_weight': None,
                'product_addt_info': 'Dviguboje kainodaroje nurodyta mažesnė įprasta kaina ir (ar) nuolaida taikoma su AČIŪ kortele.',
                'product_img_orig': 'https://dummyimage.com/400x400',
                'product_img_local': 'https://dummyimage.com/400x400',
                'is_active': True,
                'valid_from': datetime.now(),
                'valid_until': datetime.now() + timedelta(days=7),
                'created_method': Offer.MAN,
                'updated_method': Offer.MAN,
                'deactivated_method': Offer.MAN,
                'category': Category.objects.get(id='1'),
                'supermarket': Supermarket.objects.get(name='maxima'),
                'abst_product': None,
            },
            {
                'product_name': 'Malta kava PAULIG PRESIDENTTI',
                'product_brand': 'PAULIG PRESIDENTTI',
                'product_descr': 'Galioja: 05.01 - 05.07',
                'product_price': 4.69,
                'product_discount': None,
                'product_weight': None,
                'product_addt_info': '500 g, 9,38 Eur/kg',
                'product_img_orig': 'https://dummyimage.com/400x400',
                'product_img_local': 'https://dummyimage.com/400x400',
                'is_active': True,
                'valid_from': datetime.now(),
                'valid_until': datetime.now() + timedelta(days=7),
                'created_method': Offer.MAN,
                'updated_method': Offer.MAN,
                'deactivated_method': Offer.MAN,
                'category': Category.objects.get(id='5'),
                'supermarket': Supermarket.objects.get(name='iki'),
                'abst_product': None,
            },
             {
                'product_name': 'Avokadams',
                'product_brand': None,
                'product_descr': 'Tik 05.02 - 05.08',
                'product_price': None,
                'product_discount': 40,
                'product_weight': None,
                'product_addt_info': '5 rūšių. Ir IKI EXPRESS',
                'product_img_orig': 'https://dummyimage.com/400x400',
                'product_img_local': 'https://dummyimage.com/400x400',
                'is_active': True,
                'valid_from': datetime.now(),
                'valid_until': datetime.now() + timedelta(days=7),
                'created_method': Offer.MAN,
                'updated_method': Offer.MAN,
                'deactivated_method': Offer.MAN,
                'category': Category.objects.get(id='1'),
                'supermarket': Supermarket.objects.get(name='iki'),
                'abst_product': None,
            },
            {
                'product_name': 'Žaliosios besėklės vynuogės',
                'product_brand': None,
                'product_descr': '5.01. - 5.07',
                'product_price': 1.23,
                'product_discount': 55,
                'product_weight': None,
                'product_addt_info': 'Parduodama 500 g pakuotėmis',
                'product_img_orig': 'https://dummyimage.com/400x400',
                'product_img_local': 'https://dummyimage.com/400x400',
                'is_active': True,
                'valid_from': datetime.now(),
                'valid_until': datetime.now() + timedelta(days=7),
                'created_method': Offer.MAN,
                'updated_method': Offer.MAN,
                'deactivated_method': Offer.MAN,
                'category': Category.objects.get(id='1'),
                'supermarket': Supermarket.objects.get(name='lidl'),
                'abst_product': None,
            },
        ]
        # create some offers/deals
        for dict_i in offers:
            try:
                is_existing = Offer.objects.get(product_name=dict_i['product_name'])
            except Offer.DoesNotExist:
                is_existing = False

            if is_existing:
                continue

            offer = Offer(**dict_i)
            try:
                offer.save()
            except IntegrityError as e:
                logger.warning(e)

        self.stdout.write(self.style.SUCCESS('Successfully populated the Offers table with dummy data.'))
