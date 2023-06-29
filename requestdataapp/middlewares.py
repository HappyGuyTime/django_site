# from django.http import HttpRequest, HttpResponse
# from datetime import datetime

# def set_useragent_on_request_middleware(get_response):
#     print('initial call')

#     def middleware(request: HttpRequest):
#         print('before get response')
#         request.user_agent = request.META['HTTP_USER_AGENT']
#         response = get_response(request)
#         print('after get response')
#         return response

#     return middleware


# class CountRequestsMiddleware:
#     def __init__(self, get_response) -> None:
#         self.get_response = get_response
#         self.requsts_count = 0
#         self.responses_count = 0
#         self.exceptions_count = 0
#         self.waiting_time = 5
#         self.ip_addresses = dict()


#     def __call__(self, request: HttpRequest):
#         current_ip = str(request.META['REMOTE_ADDR'])

#         if self.ip_addresses.get(current_ip) is None:
#             self.ip_addresses[current_ip] = (request.path, datetime.now().second)
#         elif (
#             (self.ip_addresses[current_ip][1] + self.waiting_time > datetime.now().second) and 
#             (self.ip_addresses[current_ip][0] == request.path) and 
#             (self.requsts_count > 3)
#             ):
#             return HttpResponse("<h1>Large number of requests, please try again later</h1>")
#         else:
#             del self.ip_addresses[current_ip]
        
#         self.requsts_count += 1
#         self.responses_count += 1
#         print('Requests count', self.requsts_count)
#         print('Responses count', self.responses_count)

#         response = self.get_response(request)
#         return response


#     def process_exception(self, request: HttpRequest, exception: Exception):
#         self.exceptions_count += 1
#         print(f'got {self.exceptions_count} exceptions so far')
