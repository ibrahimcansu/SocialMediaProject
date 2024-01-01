from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('signout', views.signout, name='signout'),
    path('search', views.search, name='search'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('setting/<int:pk>', views.setting, name='setting'),
    path('like/<str:pk>', views.like, name='like'),
]
