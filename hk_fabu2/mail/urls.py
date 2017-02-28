from django.conf.urls import patterns,include,url
from mail import views

urlpatterns = [
	url(r'^$', views.index),

]