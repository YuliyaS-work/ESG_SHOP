from django.http import Http404
from django.shortcuts import redirect
from django.conf import settings

class AppendSlashFixMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        # Разбиваем путь на сегменты
        segments = [seg for seg in path.split('/') if seg]
        # 1. Если сегментов больше 3 — сразу 404
        if len(segments) > 3:
            raise Http404()

        # 2. Если сегментов 3 или меньше, но нет слэша — добавляем
        if not path.endswith('/') and '.' not in path:
            return redirect(path + '/', permanent=True)

        return self.get_response(request)
