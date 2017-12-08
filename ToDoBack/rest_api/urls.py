from django.conf.urls import url
from rest_api import views

urlpatterns = [
    url(r"^sign_up/$", views.sign_up),
    url(r"^sign_in/$", views.sign_in),
    url(r"^create_project/$", views.create_project),
    url(r"^create_task/$", views.create_task)
]