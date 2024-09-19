from django.urls import include, path

from . import views

app_name = "politeum"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("create/country", views.NewCountryView.as_view(), name="new_country"),
    path("success", views.SuccessView.as_view(), name="success")
]