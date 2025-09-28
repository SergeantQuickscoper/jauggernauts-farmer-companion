from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.test_view, name='handle_speech'),
    # path('', views.handle_speech, name='handle_speech'),
]