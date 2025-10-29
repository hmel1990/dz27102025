from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.core.cache import cache
from django.urls import reverse
from .apps import TasksappConfig
from .import views


class CachedQueryParamsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request:HttpRequest):
        cache_key = "/data/item/42/"
        if cache_key in request.path :
            if cache.has_key (cache_key, version=1):
                return cache.get(cache_key, version=1)
            else:
                response = views.result(request)
                cache.set(cache_key, response, 120,1)
                return response
        return self.get_response(request)
    
class CachedQueryNumberMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request:HttpRequest):
        cache_key = "/restricted-area/"
        if cache_key in request.path:
            request_count = cache.get(cache_key, 0)
            if request_count>=5:
                return HttpResponse("Too many requests", status=429)
            cache.set(cache_key, request_count + 1, timeout=60)
        return self.get_response(request)


