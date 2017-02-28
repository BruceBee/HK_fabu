from django.conf.urls import patterns,include,url
from projectinfo import views

urlpatterns = [
	url(r'^$', views.projectinfo),
	url(r'^addserver/', views.addserver),
	url(r'^addmodule/', views.addmodule),
	
	url(r'^getserverlist/', views.getserverlist),
	url(r'^rsynserverinfo/', views.rsynserverinfo),
	url(r'^uptime/', views.uptime),

	



	url(r'^serverinfo/(\w+)*/$', views.serverinfo),


	url(r'^GetServerInfoList/', views.GetServerInfoList),
	url(r'^GetServerInfoCount/', views.GetServerInfoCount),


	url(r'^GetProjectInfoList/', views.GetProjectInfoList),
	url(r'^GetProjectInfoCount/', views.GetProjectInfoCount),

	
	url(r'^GetModuleInfoList/', views.GetModuleInfoList),
	url(r'^GetModuleInfoCount/', views.GetModuleInfoCount),

	url(r'^projectupdate/', views.projectupdate),
	url(r'^projectswitch/', views.projectswitch),

]