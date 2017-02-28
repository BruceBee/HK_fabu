from django.conf.urls import patterns,include,url
from review import views

urlpatterns = [
	url(r'^$', views.review),
	url(r'^review_handle/(\w+)*/$', views.review_handle),

	url(r'^review_publish/', views.review_publish),
	url(r'^publish_report/(\w+)*/$', views.publish_report),
	url(r'^publish_cancle/', views.publish_cancle),

	url(r'^PreViewList/', views.PreViewList),
	url(r'^PreViewListPageCount/', views.PreViewListPageCount),

	url(r'^ReviewActionList/', views.ReviewActionList),
	url(r'^ReviewActionListPageCount/', views.ReviewActionListPageCount),

	url(r'^DownloadReport/', views.DownloadReport),
	url(r'^Downloadaction/(\w+)*/$', views.Downloadaction),

	url(r'^GetPublishlist/', views.GetPublishlist),
	url(r'^GetPublishlistPageCount/', views.GetPublishlistPageCount),

]