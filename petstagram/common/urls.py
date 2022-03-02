from django.urls import path, include

from petstagram.common.views import landing_page

urlpatterns = [
    path("", landing_page, name='landing page'),
]