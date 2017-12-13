from django.conf.urls import url
from rest_api import views

urlpatterns = [
    url(r"^sign_up/$", views.sign_up),
    url(r"^sign_in/$", views.sign_in),
    url(r"^create_project/$", views.create_project),
    url(r"^change_project/$", views.change_project),
    url(r"^delete_project/$", views.delete_project),
    url(r"^get_projects/$", views.get_projects),
    url(r"^create_task/$", views.create_task),
    url(r"^get_tasks_for_today/$", views.get_tasks_for_today),
    url(r"^get_tasks_for_project/$", views.get_tasks_for_project),
    url(r"^get_tasks_for_7_days/$", views.get_tasks_for_7_days),
    url(r"^get_done_tasks/$", views.get_done_tasks),
    url(r"^delete_task/$", views.delete_task),
    url(r"^change_task/$", views.change_task),
]