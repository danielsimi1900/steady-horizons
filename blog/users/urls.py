from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import SignupView, CustomLoginView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='post_list'), name='logout'),
]
