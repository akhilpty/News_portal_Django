from django.urls import path
from . import views

urlpatterns = [
     path("loginapi/", views.loginapi, name="loginapi"),
     path("signupapi/", views.signupapi, name="signupapi"),
     path("listapi/", views.listapi, name="listapi"),
     path("addapi/", views.addapi, name="addapi"),
     path("updatenewsapi/<int:id>", views.updatenewsapi, name="updatenewsapi"),
     path("deletenewsapi/<int:id>", views.deletenewsapi, name="deletenewsapi"),
     path("searchapi", views.searchapi, name="searchapi"),
]
