from django.urls import path
from petstagram.accounts.views import logout_user, RegisterView, ProfileFormView, LoginUserView

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='log in user'),
    path('logout/', logout_user, name='log out user'),
    path('register/', RegisterView.as_view(), name='register user'),
    path('profile/', ProfileFormView.as_view(), name='profile details'),
]