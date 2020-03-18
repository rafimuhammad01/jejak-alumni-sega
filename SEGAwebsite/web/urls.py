from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from web.views import StatistikUnivChartView, StatistikJalurChartView

urlpatterns = [
    path('', views.beranda, name="web-Beranda"),
    path('profile/<username>/', views.profile, name="web-Profile"),
    path('profile/edit/<username>/', views.editProfile, name="web-EditProfile"),
    path('Statistik/Universitas', views.statistikUniv, name="web-StatistikByUniv"),
    path('Statistik/JalurMasuk', views.statistikJalur, name="web-StatistikByJalur"),
    path('aboutUs' , views.aboutUs, name="web-aboutUs"), 
    path('register/', views.register, name="web-Register"),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)