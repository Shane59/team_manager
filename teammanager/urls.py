from django.urls import path

from . import views

app_name= "teammanager"
urlpatterns = [
  path("", views.MemberView.as_view(), name="members"),
  path("edit/<int:pk>", views.EditView.as_view(), name="edit"),
  path("add", views.AddView.as_view(), name="add"),
  path("add_member", views.add_member, name="add_member"),
  path("edit_member/<int:pk>", views.edit_member, name="edit_member"),
  path("delete_member/<int:pk>", views.delete_member, name="delete_member")
]
