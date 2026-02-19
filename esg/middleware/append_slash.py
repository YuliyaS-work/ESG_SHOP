import re

from django.http import Http404
from django.shortcuts import redirect

SEGMENT_RE = re.compile(r'^[a-zA-Z0-9._-]+$')

class AppendSlashFixMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info

        # Разбиваем путь на сегменты
        segments = [seg for seg in path.split('/') if seg]

        # 1. Проверяем каждый сегмент регуляркой
        for seg in segments:
            if not SEGMENT_RE.match(seg):
                raise Http404

        # 2. Если нет слэша — добавляем
        if not path.endswith('/') and '.' not in path:
            return redirect(path + '/', permanent=True)

        return self.get_response(request)