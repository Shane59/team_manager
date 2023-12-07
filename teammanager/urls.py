from django.urls import path

from . import views

app_name= "teammanager"
urlpatterns = [
  path("", views.MemberView.as_view(), name="index"),
  path("edit/<int:pk>", views.EditView.as_view(), name="edit"),
  path("add", views.AddView.as_view(), name="add"),
  path("delete_member/<int:pk>", views.DeleteMember.as_view(), name="delete_member")
]
