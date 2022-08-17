from django.urls import path

from .views import homePageView, sendView

urlpatterns = [
    path('', homePageView, name='home'),
    path('send/', sendView, name='send'),
]