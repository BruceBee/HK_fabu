from django.conf.urls import patterns,include,url
from softwaretest import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^LastTestInfo/', views.LastTestInfo),
	url(r'^SoftwareTestList/', views.SoftwareTestList),
	url(r'^SoftwareTestPageCount/', views.SoftwareTestPageCount),

	url(r'^SoftwareTestSearchList/', views.SoftwareTestSearchList),
	url(r'^SoftwareTestPageSearchCount/', views.SoftwareTestPageSearchCount),

	url(r'^TestHandle/(\w+)*/$', views.TestHandle),
	url(r'^GetLastTenPublishInfo/', views.GetLastTenPublishInfo),

	url(r'^GetLastTenTestInfo/', views.GetLastTenTestInfo),
	url(r'^GetActionListPageCount/', views.GetActionListPageCount),
	url(r'^GetActionList/', views.GetActionList),

	url(r'^GetActionSearchListPageCount/', views.GetActionSearchListPageCount),
	url(r'^GetActionSearchList/', views.GetActionSearchList),
	
	url(r'^TestReport/(\w+)*/$', views.TestReport),

	url(r'^EndTest/', views.EndTest),
	url(r'^.*/', views.Last),


	# url(r'^review_handle/(\w+)*/$', views.review_handle),

	# url(r'^review_publish/', views.review_publish),
	# url(r'^publish_report/(\w+)*/$', views.publish_report),

	# url(r'^PreViewList/', views.PreViewList),
	# url(r'^PreViewListPageCount/', views.PreViewListPageCount),

	# url(r'^ReviewActionList/', views.ReviewActionList),
	# url(r'^ReviewActionListPageCount/', views.ReviewActionListPageCount),

	# url(r'^DownloadReport/', views.DownloadReport),
	# url(r'^Downloadaction/(\w+)*/$', views.Downloadaction),

	# url(r'^GetPublishlist/', views.GetPublishlist),
	# url(r'^GetPublishlistPageCount/', views.GetPublishlistPageCount),

]