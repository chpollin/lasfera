from django.shortcuts import render

from pages.models import AboutPage

# def about(request):
#     about_page = AboutPage.objects.live().first()

#     return render(
#         request,
#         "base.html",
#         {
#             "about_page": about_page,
#         },
#     )
