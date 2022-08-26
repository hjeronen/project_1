from django.urls import path

from .views import homePageView, sendView, deleteView

urlpatterns = [
    path('', homePageView, name='home'),
    path('send/', sendView, name='send'),
    path('delete/<int:message_id>', deleteView, name='delete'),
]