from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.beranda, name="web-Beranda"),
    path('profile/<username>/', views.profile, name="web-Profile"),
    path('profile/edit/<username>/', views.editProfile, name="web-EditProfile"),
    path('statistik/', views.statistik, name="web-Statistik"),
    path('register/', views.register, name="web-Register"),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)