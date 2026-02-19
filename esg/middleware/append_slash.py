import re
from django.shortcuts import redirect, render

SEGMENT_RE = re.compile(r'^[a-zA-Z0-9._-]+$')

class AppendSlashFixMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info

        # Разбиваем путь на сегменты
        segments = [seg for seg in path.split('/') if seg]

        # 1. Если сегментов больше 3 — сразу 404
        if len(segments) > 3:
            return render(request, '404.html', status=404)

        # 2. Проверяем каждый сегмент регуляркой
        for seg in segments:
            if not SEGMENT_RE.match(seg):
                return render(request, '404.html', status=404)

        # 3. Если нет слэша — добавляем
        if not path.endswith('/') and '.' not in path:
            return redirect(path + '/', permanent=True)

        return self.get_response(request)