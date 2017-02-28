"""hk_fabu2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import patterns,include,url
from django.contrib import admin
# from django.contrib import admin
from index import views as index_views
from projectinfo import views as projectinfo_views
from rollback import views as rollback_views
from startstoprestart import views as startstoprestart_views
from haproxyedit import views as haproxyedit_views
from showlogs import views as showlogs_views
from review import views as review_views
from publishmanage import views as publish_views


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$', index_views.index, name='index'),
    url(r'^LoadDashboard/', index_views.LoadDashboard, name='LoadDashboard'),
    url(r'^LoadNotice/', index_views.LoadNotice, name='LoadNotice'),
    url(r'^LoadDisk/', index_views.LoadDisk, name='LoadDisk'),
    
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', index_views.login, name='login'),
    # url(r'^test/$', index_views.test, name='test'),
    url(r'^fileupload/$', index_views.fileupload, name='fileupload'),
    url(r'^Deployment/$', index_views.Deployment, name='Deployment'),
    url(r'^Deployment/check_md5/$', index_views.check_md5, name='check_md5'),
    
    url(r'^PublishList/$', publish_views.PublishList, name='PublishList'),
    url(r'^Deployment/GetProjectServerIP/$', index_views.GetProjectServerIP, name='GetProjectServerIP'),
    url(r'^projectinfo/$', projectinfo_views.projectinfo, name='projectinfo'),

    # url(r'^review/$', review_views.review, name='review'),
    # url(r'^result/$', review_views.result, name='result'),
    # url(r'^GetPublishlist/$', review_views.GetPublishlist, name='GetPublishlist'),
    # url(r'^GetPublishlistPageCount/$', review_views.GetPublishlistPageCount, name='GetPublishlistPageCount'),

    # url(r'^review/review_handle/(\w+)*/$', review_views.review_handle, name='review_handle'),
    # url(r'^review_publish/$', review_views.review_publish, name='review_publish'),
    # url(r'^review/publish_report/(\w+)*/$', review_views.publish_report, name='publish_report'),
    # url(r'^PreViewList/$', review_views.PreViewList, name='PreViewList'),
    # url(r'^PreViewListPageCount/$', review_views.PreViewListPageCount, name='PreViewListPageCount'),
    
    # url(r'^ReviewActionList/$', review_views.ReviewActionList, name='ReviewActionList'),
    # url(r'^ReviewActionListPageCount/$', review_views.ReviewActionListPageCount, name='ReviewActionListPageCount'),
    
    # url(r'^DownloadReport/$', review_views.DownloadReport, name='DownloadReport'),
    # url(r'^Downloadaction/(\w+)*/$', review_views.Downloadaction, name='Downloadaction'),
    # url(r'^testDownload/$', review_views.testDownload, name='testDownload'),
    

    
    url(r'^GetProjectServerIP/$', index_views.GetProjectServerIP, name='GetProjectServerIP'),
    url(r'^GetReviewer/$', index_views.GetReviewer, name='GetReviewer'),
    
    url(r'^logout/$', index_views.logout, name='logout'),
    url(r'^rollback/$', rollback_views.rollback, name='rollback'),
    url(r'^GetBackupName/$', rollback_views.get_backup_name, name='get_backup_name'),
    url(r'^startstoprestart/$', startstoprestart_views.startstoprestart, name='startstoprestart'),
    url(r'^haproxyedit/$', haproxyedit_views.haproxyedit, name='haproxyedit_views'),
    url(r'^showlogs/$', showlogs_views.showlogs, name='showlogs'),


    url(r'^projectinfo/',include('projectinfo.urls')),
    url(r'^review/',include('review.urls')),
    url(r'^softwaretest/',include('softwaretest.urls')),
    url(r'^log/',include('log.urls')),
    url(r'^mail/',include('mail.urls')),
    url(r'^usermanage/',include('usermanage.urls')),
    url(r'^processmanage/',include('processmanage.urls')),
    url(r'^', index_views.test, name='test'),

]


