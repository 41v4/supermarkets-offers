import logging
import os

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from offers.models import (Category, Notificator, Subcategory,
                           SubcategoryProductNames, Supermarket)

logger = logging.getLogger('offer')

class Command(BaseCommand):
    help = 'Populate the Category, Subcategory, SubcategoryProductNames and Supermarkets table with initial data'

    def handle(self, *args, **options):
        category_init_data = [
            {
                "id": 1,
                "name": "Daržoves ir vaisiai",
                "url": "darzoves-ir-vaisiai",
                "priority": 1,
                "subcategories": [
                    {"priority": 1, "name": "Daržoves ir grybai", "url": "darzoves ir grybai"},
                    {"priority": 2, "name": "Vaisiai ir uogos", "url": "vaisiai ir uogos"}
                ]
            },
            {
                "id": 2,
                "name": "Pieno gaminiai ir kiaušiniai",
                "url": "pieno-gaminiai-ir-kiausiniai",
                "priority": 2,
                "subcategories": [
                    {"priority": 1, "name": "Pienas", "url": "pienas"},
                    {"priority": 2, "name": "Sviestas, margarinas ir riebalai", "url": "sviestas-margarinas-ir-riebalai"},
                    {"priority": 3, "name": "Produktai be laktozės", "url": "produktai-be-laktozes"},
                    {"priority": 4, "name": "Grietinė ir grietinėlė", "url": "grietine-ir-grietinele"},
                    {"priority": 5, "name": "Sūris", "url": "suris"},
                    {"priority": 6, "name": "Majonezas", "url": "majonezas"},
                    {"priority": 7, "name": "Kefyras, rūgpienis ir pasukos", "url": "kefyras-rugpienis-ir-pasukos"},
                    {"priority": 8, "name": "Jogurtai ir desertai", "url": "jogurtai-ir-desertai"},
                    {"priority": 9, "name": "Užtepėlės ir humusai", "url": "uztepeles-ir-humusai"},
                    {"priority": 10, "name": "Varškės produktai", "url": "varskes-produktai"},
                    {"priority": 11, "name": "Kiaušiniai", "url": "kiausiniai"},
                ]
            },
            {
                "id": 3,
                "name": "Duonos gaminiai ir konditerija",
                "url": "duonos-gaminiai-ir-konditerija",
                "priority": 3,
                "subcategories": [
                    {"priority": 1, "name": "Šviežiai kepti duonos gaminiai", "url": "svieziai-kepti-duonos-gaminiai"},
                    {"priority": 2, "name": "Džiuvėsiai, riestainiai, meduoliai ir javinukai", "url": "dziuvesiai-riestainiai-meduoliai-ir-javinukai"},
                    {"priority": 3, "name": "Duona", "url": "duona"},
                    {"priority": 4, "name": "Konditerijos gaminiai", "url": "konditerijos-gaminiai"},
                    {"priority": 5, "name": "Duonos, pyragai, keksai ir keksiukai", "url": "duonos-pyragai-keksai-ir-keksiukai"},
                    {"priority": 6, "name": "Duonos pakaitalai", "url": "duonos-pakaitalai"},
                    {"priority": 7, "name": "Bandelės ir spurgos", "url": "bandeles-ir-spurgos"},
                ]
            },
            {
                "id": 4,
                "name": "Mėsa, žuvis ir kulinarija",
                "url": "mesa-zuvis-ir-kulinarija",
                "priority": 4,
                "subcategories": [
                    {"priority": 1, "name": "Šviežia mėsa", "url": "sviezia-mesa"},
                    {"priority": 2, "name": "Šviežia paukštiena", "url": "sviezia-paukstiena"},
                    {"priority": 3, "name": "Šviežios mėsos ir paukštienos pusgaminiai", "url": "sviezios-mesos-ir-paukstienos-pusgaminiai"},
                    {"priority": 4, "name": "Mėsos ir paukštienos gaminiai", "url": "mesos-ir-paukstienos-gaminiai"},
                    {"priority": 5, "name": "Šviežios žuvys ir jūrų gėrybės", "url": "sviezios-zuvys-ir-juru-gerybes"},
                    {"priority": 6, "name": "Žuvų gaminiai", "url": "zuvu-gaminiai"},
                    {"priority": 7, "name": "Kulinarija", "url": "kulinarija"},
                ]
            },
            {
                "id": 5,
                "name": "Bakalėja",
                "url": "bakaleja",
                "priority": 5,
                "subcategories": [
                    {"priority": 1, "name": "Makaronai", "url": "makaronai"},
                    {"priority": 2, "name": "Ankštinės daržovės", "url": "ankstines-darzoves"},
                    {"priority": 3, "name": "Sausi pusryčiai, dribsniai ir javainių batonėliai", "url": "sausi-pusryciai-dribsniai-ir-javainiu-batoneliai"},
                    {"priority": 4, "name": "Užkandžiai", "url": "uzkandziai"},
                    {"priority": 5, "name": "Riešutai, sėklos, džiovinti vaisiai, uogos ir daržovės", "url": "riesutai-seklos-dziovinti-vaisiai-uogos-ir-darzoves"},
                    {"priority": 6, "name": "Padažai", "url": "padazai"},
                    {"priority": 7, "name": "Konservuotas maistas", "url": "konservuotas-maistas"},
                    {"priority": 8, "name": "Miltai ir miltų mišiniai", "url": "miltai-ir-miltu-misiniai"},
                    {"priority": 9, "name": "Kruopos", "url": "kruopos"},
                    {"priority": 10, "name": "Prieskoniai", "url": "prieskoniai"},
                    {"priority": 11, "name": "Greitai paruošiamas maistas", "url": "greitai-paruosiamas-maistas"},
                    {"priority": 12, "name": "Arbata", "url": "arbata"},
                    {"priority": 13, "name": "Pasaulio virtuvės", "url": "pasaulio-virtuves"},
                    {"priority": 14, "name": "Cukrus ir saldikliai", "url": "cukrus-ir-saldikliai"},
                    {"priority": 15, "name": "Aliejus ir actas", "url": "aliejus-ir-actas"},
                    {"priority": 16, "name": "Saldumynai", "url": "saldumynai"},
                    {"priority": 17, "name": "Priedai maistui ruošti", "url": "priedai-maistui-ruosti"},
                    {"priority": 18, "name": "Kava, kavos gerimai ir kakava", "url": "kava-kavos-gerimai-ir-kakava"},
                    {"priority": 19, "name": "Specialusis maistas", "url": "specialusis-maistas"},
                ]
            },
            {
                "id": 6,
                "name": "Šaldytas maistas",
                "url": "saldytas-maistas",
                "priority": 6,
                "subcategories": [
                    {"priority": 1, "name": "Šaldytos daržovės, grybai ir uogos", "url": "saldytos-darzoves-grybai-ir-uogos"},
                    {"priority": 2, "name": "Šaldyta žuvis ir jūrų gėrybės", "url": "saldyta-zuvis-ir-juru-gerybes"},
                    {"priority": 3, "name": "Šaldyti kulinarijos ir konditerijos gaminiai", "url": "saldyti-kulinarijos-ir-konditerijos-gaminiai"},
                    {"priority": 4, "name": "Ledai ir ledo kubeliai", "url": "ledai-ir-ledo-kubeliai"},
                    {"priority": 5, "name": "Šaldyta mėsa", "url": "saldyta-mesa"},
                ]
            },
            {
                "id": 7,
                "name": "Gėrimai",
                "url": "gerimai",
                "priority": 7,
                "subcategories": [
                    {"priority": 1, "name": "Vanduo", "url": "vanduo"},
                    {"priority": 2, "name": "Gaivieji gėrimai", "url": "gaivieji-gerimai"},
                    {"priority": 3, "name": "Sultys, nektarai, sulčių gėrimai ir beržų sula", "url": "sultys-nektarai-sulciu-gerimai-ir-berzu-sula"},
                    {"priority": 4, "name": "Nealkoholiniai gėrimai", "url": "nealkoholiniai-gerimai"},
                ]
            },
            {
                "id": 8,
                "name": "Kūdikių ir vaikų prekės",
                "url": "kudikiu-ir-vaiku-prekes",
                "priority": 8,
                "subcategories": [
                    {"priority": 1, "name": "Pieno mišiniai", "url": "pieno-misiniai"},
                    {"priority": 2, "name": "Kūdikių košės", "url": "kudikiu-koses"},
                    {"priority": 3, "name": "Kūdikių gėrimai ir užkandžiai", "url": "kudikiu-gerimai-ir-uzkandziai"},
                    {"priority": 4, "name": "Vaisinės ir desertinės tyrelės", "url": "vaisines-ir-desertines-tyreles"},
                    {"priority": 5, "name": "Mėsos ir daržovių tyrelės", "url": "mesos-ir-darzoviu-tyreles"},
                    {"priority": 6, "name": "Vaikų higienos prekės", "url": "vaiku-higienos-prekes"},
                    {"priority": 7, "name": "Sauskelnės ir servetėlės", "url": "sauskelnes-ir-serveteles"},
                    {"priority": 8, "name": "Kūdikių ir vaikų žaislai", "url": "kudikiu-ir-vaiku-zaislai"},
                    {"priority": 9, "name": "Lego konstruktoriai", "url": "lego-konstruktoriai"},
                    {"priority": 10, "name": "Priežiūros prekės", "url": "prieziuros-prekes"},
                ]
            },
            {
                "id": 9,
                "name": "Kosmetika ir higiena",
                "url": "kosmetika-ir-higiena",
                "priority": 9,
                "subcategories": [
                    {"priority": 1, "name": "Burnos higienos priemonės", "url": "burnos-higienos-priemones"},
                    {"priority": 2, "name": "Veido priežiūros priemonės", "url": "veido-prieziuros-priemones"},
                    {"priority": 3, "name": "Dezodorantai", "url": "dezodorantai"},
                    {"priority": 4, "name": "Kūno priežiūros priemonės", "url": "kuno-prieziuros-priemones"},
                    {"priority": 5, "name": "Dekoratyvinė kosmetika", "url": "dekoratyvine-kosmetika"},
                    {"priority": 6, "name": "Medicinos prekės", "url": "medicinos-prekes"},
                    {"priority": 7, "name": "Rankų ir pėdų odos priežiūros priemonės", "url": "ranku-ir-pedu-odos-prieziuros-priemones"},
                    {"priority": 8, "name": "Skutimosi prekės", "url": "skutimosi-prekes"},
                    {"priority": 9, "name": "Kvepalai", "url": "kvepalai"},
                    {"priority": 10, "name": "Plaukų priežiūros priemonės", "url": "plauku-prieziuros-priemones"},
                    {"priority": 11, "name": "Intymios higienos prekės", "url": "intymios-higienos-prekes"},
                ]
            },
            {
                "id": 10,
                "name": "Švaros ir gyvūnų prekės",
                "url": "svaros-ir-gyvunu-prekes",
                "priority": 10,
                "subcategories": [
                    {"priority": 1, "name": "Gyvūnų prekįs", "url": "gyvunu-prekes"},
                    {"priority": 2, "name": "Indų plovikliai", "url": "indu-plovikliai"},
                    {"priority": 3, "name": "Popieriniai gaminiai", "url": "popieriniai-gaminiai"},
                    {"priority": 4, "name": "Priemonės valymui", "url": "priemones-valymui"},
                    {"priority": 5, "name": "Buitinės chemijos prekės", "url": "buitines-chemijos-prekes"},
                    {"priority": 6, "name": "Skalbimo priemonės", "url": "skalbimo-priemones"},
                ]
            },
            {
                "id": 11,
                "name": "Namai ir laisvalaikis",
                "url": "namai-ir-laisvalaikis",
                "priority": 11,
                "subcategories": [
                    {"priority": 1, "name": "Buitinė technika ir elektronika", "url": "buitine-technika-ir-elektronika"},
                    {"priority": 2, "name": "Automobilių prekės", "url": "automobiliu-prekes"},
                    {"priority": 3, "name": "Laisvalaikio prekės", "url": "laisvalaikio-prekes"},
                    {"priority": 4, "name": "Virtuvės ir stalo serviravimo reikmenys", "url": "virtuves-ir-stalo-serviravimo-reikmenys"},
                    {"priority": 5, "name": "Mokyklinės prekės", "url": "mokyklines-prekes"},
                    {"priority": 6, "name": "Laikraščiai, žurnalai, knygos", "url": "laikrasciai-zurnalai-knygos"},
                    {"priority": 7, "name": "Maisto ruošimo ir laikymo indai", "url": "maisto-ruosimo-ir-laikymo-indai"},
                    {"priority": 8, "name": "Kojinės ir apatinis trikotažas", "url": "kojines-ir-apatinis-trikotazas"},
                    {"priority": 9, "name": "Namų apyvokos reikmenys", "url": "namu-apyvokos-reikmenys"},
                    {"priority": 10, "name": "Augalai ir jų priežiūra", "url": "augalai-ir-ju-prieziura"},
                ]
            },
        ]
        # create some categories and subcategories
        for category_i in category_init_data:
            cat_id = category_i["id"]
            cat_name = category_i["name"]
            cat_url = category_i["url"]
            cat_priority = category_i["priority"]
            category = Category(id=cat_id, name=cat_name, url=cat_url, priority=cat_priority)
            try:
                category.save()
            except IntegrityError as e:
                logger.warning(e)
            
            subcategories = category_i["subcategories"]
            subcategory_objects = []  # Store the subcategory objects in a list
            
            for subcategory_i in subcategories:
                subcat_name = subcategory_i["name"]
                subcat_url = subcategory_i["url"]
                subcat_priority = subcategory_i["priority"]
                category_obj = Category.objects.get(id=cat_id)
                subcategory = Subcategory(name=subcat_name, url=subcat_url, category=category_obj, priority=subcat_priority)
                subcategory_objects.append(subcategory)  # Add the subcategory object to the list
            
            try:
                Subcategory.objects.bulk_create(subcategory_objects)  # Save all subcategories in one database query
            except IntegrityError as e:
                logger.warning(e)


        self.stdout.write(self.style.SUCCESS('Successfully populated Category, Subcategory tables with initial data.'))

        subcat_products_dir = "product_names/"
        if os.path.exists(subcat_products_dir):
            subcategory_product_name_objects = []
            fns = os.listdir(subcat_products_dir)
            for fn in fns:
                fp = os.path.join(subcat_products_dir, fn)
                cat_id = fn.strip(".txt").split("_")[0]
                subcat_id = fn.strip(".txt").split("_")[1]
                with open(fp, "r") as f:
                    lines = set([i.strip() for i in f.readlines()])
                for name in lines:
                    subcategory = Subcategory.objects.get(category=Category.objects.get(id=cat_id), priority=subcat_id)
                    subcat_product_name = SubcategoryProductNames(name=name, subcategory=subcategory)
                    subcategory_product_name_objects.append(subcat_product_name)
            try:
                SubcategoryProductNames.objects.bulk_create(subcategory_product_name_objects)
            except IntegrityError as e:
                logger.warning(e)

            self.stdout.write(self.style.SUCCESS('Successfully populated the SubcategoryProductNames table with initial data.'))
                

        supermarkets = [
            {"name": "maxima", "website_url": "https://www.maxima.lt/", "descr": "Description of Maxima supermarket"},
            {"name": "iki", "website_url": "https://iki.lt/", "descr": "Description of Iki supermarket"},
            {"name": "lidl", "website_url": "https://www.lidl.lt/", "descr": "Description of Lidl supermarket"},
            {"name": "norfa", "website_url": "https://www.norfa.lt/", "descr": "Description of Norfa supermarket"},
            {"name": "rimi", "website_url": "https://www.rimi.lt/", "descr": "Description of Rimi supermarket"}
        ]

        # create some categories
        for dict_i in supermarkets:
            supermarket = Supermarket(**dict_i)
            try:
                supermarket.save()
            except IntegrityError as e:
                logger.warning(e)

        self.stdout.write(self.style.SUCCESS('Successfully populated the Supermarkets table with initial data.'))

        notificators = [
            {"name": "email"},
            {"name": "telegram"},
        ]

        # create some notificators
        for dict_i in notificators:
            notificator = Notificator(**dict_i)
            try:
                notificator.save()
            except IntegrityError as e:
                logger.warning(e)

        self.stdout.write(self.style.SUCCESS('Successfully populated the Notificators table with initial data.'))
