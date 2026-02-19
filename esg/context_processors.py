from .models import Rubric

def rubrics_processor(request):
    try:
        return {'rubrics': Rubric.objects.all()}
    except:
        return {'rubrics': []}
