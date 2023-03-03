# from django.http import HttpResponse
# from django.utils.deprecation import MiddlewareMixin
#
# class M1(MiddlewareMixin):
#     """Middleware defined"""
#     # def process_request(self,request):
#         # if got return value,  return now!
#         # if no return value, can continue process
#         # can exclude those page that does not need session
#         # if request.path_info =="/login/":
#         #     return
#         # if request.session.get("info"):
#         #     return HttpResponse("Login successful!")
#         # return HttpResponse("Go login!")
#
#     def process_response(self,request, response):
#         print("Bye~")