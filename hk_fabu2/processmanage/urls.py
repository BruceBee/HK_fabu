from django.conf.urls import patterns,include,url
from processmanage import views

# Create your views here.
urlpatterns = [
	url(r'^$', views.index),
	url(r'^processitems/', views.processitems),
	url(r'^processitemscount/', views.processitemscount),
	url(r'^processearchcount/', views.processearchcount),
	
	
	url(r'^GetProcessInfo/', views.GetProcessInfo),


	# url(r'^GetLoginList/', views.GetLoginList),
	# url(r'^GetLoginPageCount/', views.GetLoginPageCount),

	# url(r'^GetActionList/', views.GetActionList),
	# url(r'^GetActionPageCount/', views.GetActionPageCount),

	# url(r'^GetLoginLogSearchInfo/', views.GetLoginLogSearchInfo),
	# url(r'^GetLoginLogSearchCount/', views.GetLoginLogSearchCount),

]