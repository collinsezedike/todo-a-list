from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_all_todos),
    path("add/", views.add_todo),
    path("search/", views.search_todo),
    path("todo/<int:todo_id>/", views.get_todo_by_id),
    path("complete/<int:todo_id>/", views.complete_todo),
    path("edit/<int:todo_id>/", views.edit_todo),
    path("delete/<int:todo_id>/", views.delete_todo),
]