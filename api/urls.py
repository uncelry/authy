from api.views import generate_tokens_view, refresh_tokens_view
from django.urls import path


urlpatterns = [
    path('auth/generate_tokens/', generate_tokens_view, name='generate_tokens'),
    path('auth/refresh_tokens/', refresh_tokens_view, name='refresh_tokens'),
]