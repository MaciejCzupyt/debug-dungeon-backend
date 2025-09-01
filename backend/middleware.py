# This is a fix for if the front starts receiving login alert pop-ups ever again

class SuppressBrowserAuthPopupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.startswith("/api/") and response.status_code == 401:
            response['WWW-Authenticate'] = ''
        return response