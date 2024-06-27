# myapp/urls.py

from django.urls import path
from .views import ChatGPTView

urlpatterns = [
    path('chat/', ChatGPTView.as_view(), name='chat-gpt'),
]
