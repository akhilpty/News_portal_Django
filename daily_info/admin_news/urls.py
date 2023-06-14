
from django.urls import path
from . import views

urlpatterns = [
     path("register/", views.register_admin, name="registeradmin"),
     path("login/", views.login_admin, name="loginadmin"),
     path('logout',views.logout_admin,name="logoutadmin"),
     path("", views.home.as_view(), name="homenews"),
     path("add/", views.addnews, name="addnews"),
     path("update/<int:id>",views.updatenews,name='updatenews'),
     path("detail/<int:id>",views.detailnews,name='detailnews'),
     path("mynews/",views.mynewsdetail,name='mydetailnews'),
     path("delete/<int:id>",views.deletenews,name='deletenews'),
    

]