# paste the code block above here exactly
from django.http import HttpResponse, JsonResponse

def login_view(request):
    """
    Minimal login-like endpoint.
    Later we’ll add rate limiting here.
    """
    return JsonResponse({"ok": True, "message": "Login endpoint working"})

def hello(request):
    """
    Simple test endpoint.
    """
    return HttpResponse("Hello — IP tracking is active!")
