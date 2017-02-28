from django.conf.urls import patterns,include,url
from usermanage import views

urlpatterns = [
	url(r'^$', views.index),
	# url(r'^review_handle/(\w+)*/$', views.review_handle),
	# url(r'^review_publish/', views.review_publish),
	url(r'^GetUserList/', views.GetUserList),
	url(r'^GetUserListCount/', views.GetUserListCount),

	url(r'^GetUserSearchList/', views.GetUserSearchList),
	url(r'^GetUserSearchCount/', views.GetUserSearchCount),
	
	url(r'^UserAdd/', views.UserAdd),
	url(r'^UserCheck/', views.UserCheck),
	url(r'^UserStatusSwitch/', views.UserStatusSwitch),

	

]