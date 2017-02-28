from django.conf.urls import patterns,include,url
from log import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^GetLoginList/', views.GetLoginList),
	url(r'^GetLoginPageCount/', views.GetLoginPageCount),

	url(r'^GetActionList/', views.GetActionList),
	url(r'^GetActionPageCount/', views.GetActionPageCount),

	url(r'^GetLoginLogSearchInfo/', views.GetLoginLogSearchInfo),
	url(r'^GetLoginLogSearchCount/', views.GetLoginLogSearchCount),

]