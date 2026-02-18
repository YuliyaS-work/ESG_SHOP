from django.shortcuts import redirect
from django.conf import settings

class AppendSlashFixMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        # Если путь не заканчивается слэшем и не содержит точки (файлы)
        if not path.endswith('/') and '.' not in path:
            return redirect(path + '/', permanent=True)

        return self.get_response(request)
