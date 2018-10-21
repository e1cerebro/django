from django.conf.urls import url
from first_app import views

app_name = 'first_app'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^showform/', views.showform, name='showform'),
    url(r'^newtopic/', views.newtopic, name='newtopic'),
    url(r'^register/', views.register, name='register'),
    url(r'^user_login/', views.user_login, name='user_login')
]