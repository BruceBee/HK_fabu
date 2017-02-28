#!/usr/bin/env python
# -*- coding:utf-8 -*-

import ConfigParser
from publicvar import *
from index.models import UserLoginInfo
from usermanage.models import UserInfo


def read_project_name(section=None):
    """
    从hosts文件中获取项目名
    :param section:项目名。如给定了项目名，则返回该项目的服务器列表
    :return:列表
    """
    # all_project_name = Project.objects.values_list('project_name', 'project_server')

    conf = ConfigParser.ConfigParser()
    conf.read(ansible_hosts)
    if section:
        return conf.options(section)
    return conf.sections()

#获取用户权限
def GetUserAuth(user):
    UserObject = UserInfo.objects.get(user=user)
    return UserObject.have_publish,UserObject.have_review,UserObject.have_test


# def SearchData(database_name):
#     Database_dir = {'ForReview':['id','publish_type','publish_status','publish_module','publish_filename','publish_user','review_owner','create_time','publish_serverlist','publish_detail'],
#     'ReviewAction':['publish_id','publish_type','publish_status','publish_module','publish_filename','publish_user','review_owner','create_time','review_time','review_info'],
#     'SoftwareTest':['publish_id','publish_type','publish_status','publish_module','publish_filename','publish_user','review_owner','create_time','review_time','review_info']

#     }
#     try:
#         '''
#         返回用户表查询模块配置列表
#         '''
#         k_words = request.POST.get('k_words','').encode('utf-8')
#         # return HttpResponse(k_words)
#         s_page = request.POST.get('s_page','')
#         # e_page = request.POST.get('e_page','')
#         page_size = request.POST.get('page_size','')
#         SearchData_obj = database_name.objects.filter(Q(user__contains=str(k_words)) \
#             | Q(ftp_path__contains=str(k_words)) \
#             | Q(remark__contains=str(k_words))).values().order_by('-user')[(int(s_page)-1)*int(page_size):int(s_page)*int(page_size)]

#         page_total = UserInfo.objects.filter(Q(user__contains=str(k_words)) \
#             | Q(ftp_path__contains=str(k_words)) \
#             | Q(remark__contains=str(k_words))).count()
#         # data = "{\"UserInfo_obj\":"+json.dumps(list(UserInfo_obj))+"}"

#         return SearchData_obj,page_total
#     except Exception as e:
#         return 'err_msg',e