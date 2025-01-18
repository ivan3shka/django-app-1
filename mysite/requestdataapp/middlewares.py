from django.http import HttpRequest, HttpResponse
import time

def set_useragent_on_request_middleware(get_response):
    print('init call')
    def middleware(request: HttpRequest):
        print('init before')
        request.user_agent = request.META['HTTP_USER_AGENT']
        response = get_response(request)
        print('init after')
        return response

    return middleware


class CountRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_count = 0
        self.responses_count = 0
        self.exception_count = 0

    def __call__(self, request):
        self.request_count += 1
        print(f'request_count: {self.request_count}')
        res = self.get_response(request)
        self.responses_count += 1
        print(f'responses_count: {self.responses_count}')
        return res

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exception_count += 1
        print(f'exception_count: {self.exception_count}')
        return



class ThrottlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_requests = {}
        self.time_window = 10
        self.max_requests = 5

    def __call__(self, request):
        ip_address = self.get_client_ip(request)

        current_time = time.time()

        if ip_address not in self.ip_requests:
            self.ip_requests[ip_address] = []

        self.ip_requests[ip_address] = [
            timestamp for timestamp in self.ip_requests[ip_address]
            if current_time - timestamp <= self.time_window
        ]

        self.ip_requests[ip_address].append(current_time)

        if len(self.ip_requests[ip_address]) > self.max_requests:
            return HttpResponse("Too many requests. Please slow down.",
                                status=429)

        response = self.get_response(request)
        return response

    @staticmethod
    def get_client_ip(request):
        """Извлечение IP-адреса клиента."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')


