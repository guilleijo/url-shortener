from django.urls import path

from .views import HomeView, RedirectView


urlpatterns = [
    path('', HomeView.as_view(), name='home_page'),
    path('<hash>', RedirectView.as_view(), name='redirect_view'),
]
