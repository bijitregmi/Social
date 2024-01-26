
from django.urls import path

from . import views

app_name = 'network'
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:pk>", views.profile, name="profile"),
    path('follow/<int:pk>', views.follow, name="follow"),
    path('following', views.following, name="following"),

    # API routes
    path('edit/<int:pk>', views.edit, name="edit"),
    path('like/<int:pk>', views.like, name="like")

]
