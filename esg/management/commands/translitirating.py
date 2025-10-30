import re

from django.core.management import BaseCommand
from transliterate import translit


from esg.models import *

class Command(BaseCommand):

    def handle(self, *args, **options):
        # rubrics = Rubric.objects.all()
        # for rubric in rubrics:
        #     transliterated_name = translit(rubric.rubric_name.lower(), 'ru', reversed=True)
        #     rubric.name_translit = transliterated_name
        #     rubric.save(update_fields=['name_translit'])

        electro = Electro.objects.all()
        for rubric in electro:
            transliterated_name = translit(rubric.title.lower(), 'ru', reversed=True)
            cleaned_name = re.sub(r'\(.*?\)', '', transliterated_name)
            translist = re.split(r'\s*,\s*|\s+i\s+|\s+dlja\s+|\s+' , cleaned_name)
            translit_sp = [word for word in translist if word]
            transliterated_title = ('-').join(translit_sp)
            rubric.title_translit = transliterated_title
            rubric.save(update_fields=['title_translit'])

        gas = Gas.objects.all()
        for rubric in gas:
            transliterated_name = translit(rubric.title.lower(), 'ru', reversed=True)
            cleaned_name = re.sub(r'\(.*?\)', '', transliterated_name)
            translist = re.split(r'\s*,\s*|\s+i\s+|\s+dlja\s+|\s+', cleaned_name)
            translit_sp = [word for word in translist if word]
            transliterated_title = ('-').join(translit_sp)
            rubric.title_translit = transliterated_title
            rubric.save(update_fields=['title_translit'])

        santeh = Santeh.objects.all()
        for rubric in santeh:
            transliterated_name = translit(rubric.title.lower(), 'ru', reversed=True)
            cleaned_name = re.sub(r'\(.*?\)', '', transliterated_name)
            translist = re.split(r'\s*,\s*|\s+i\s+|\s+dlja\s+|\s+', cleaned_name)
            translit_sp = [word for word in translist if word]
            transliterated_title = ('-').join(translit_sp)
            rubric.title_translit = transliterated_title
            rubric.save(update_fields=['title_translit'])
