from django.contrib import admin

# Register your models here.
from .models import *
from review.models import *
from softwaretest.models import *
from usermanage.models import *


class UserLoginInfoAdmin(admin.ModelAdmin):
	list_display =('user','password','ftp_path','remark','have_publish','have_review')
	search_fields = ['user','password','ftp_path','remark','have_publish','have_review']
	list_filter = ('user','password','ftp_path','remark','have_publish','have_review')

class ForReviewAdmin(admin.ModelAdmin):
	list_display = ('publish_status','publish_module','publish_filename','file_uploadtime','publish_user','create_time','publish_serverlist','publish_detail','review_owner')
	search_fields = ['publish_status','publish_module','publish_filename','file_uploadtime','publish_user','create_time','publish_serverlist','publish_detail','review_owner']
	list_filter = ['publish_status','publish_module','publish_filename','file_uploadtime','publish_user','create_time','publish_serverlist','publish_detail','review_owner']

class ReviewActionAdmin(admin.ModelAdmin):
	list_display = ('publish_id','publish_status','publish_module','publish_filename','file_uploadtime','publish_user','create_time','publish_serverlist','publish_detail','review_owner','review_time','review_info',)
	search_fields =['publish_id','publish_status','publish_module','publish_filename','file_uploadtime','publish_user','create_time','publish_serverlist','publish_detail','review_owner','review_time','review_info',]
	list_filter =['publish_id','publish_status','publish_module','publish_filename','file_uploadtime','publish_user','create_time','publish_serverlist','publish_detail','review_owner','review_time','review_info',]


class SoftwareTestAdmin(admin.ModelAdmin):
	list_display =('publish_id','test_user','test_starttime','test_endtime','test_detail')
	search_fields = ['publish_id','test_user','test_starttime','test_endtime']
	list_filter = ['publish_id','test_user','test_starttime','test_endtime']

class UserInfoAdmin(admin.ModelAdmin):
	list_display =('user','password','ftp_path','remark','have_publish','have_review','have_test')
	search_fields = ['user','password','ftp_path','remark','have_publish','have_review','have_test']
	list_filter = ['user','password','ftp_path','remark','have_publish','have_review','have_test']

admin.site.register(UserLoginInfo,UserLoginInfoAdmin)
admin.site.register(ForReview,ForReviewAdmin)
admin.site.register(ReviewAction,ReviewActionAdmin)
admin.site.register(SoftwareTest,SoftwareTestAdmin)
admin.site.register(UserInfo,UserInfoAdmin)
