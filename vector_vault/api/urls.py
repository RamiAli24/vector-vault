from django.urls import path

from .views import BookView

urlpatterns = [
    path("names/", BookView.as_view(), name="books"),
]
