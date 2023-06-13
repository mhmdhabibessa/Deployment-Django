from django.urls import path
from . import views
                    
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('wall', views.wall),
    path('craete-pie', views.craetePie),
    path('edit/<int:uid>', views.edit),
    path('update/<int:uid>', views.update),
    path('delete/<int:uid>', views.delete),
    path('pie-derby', views.pieDerby),
    path('vote-pie/<int:uid>', views.votePie),
    path('user/vote/<int:uid>', views.addVote),
    path('user/un-vote/<int:uid>', views.unvote),
    path('logout', views.logout),
]