# Create your views here.
# -*- coding:utf-8 -*-

from django.shortcuts import render, HttpResponse, render_to_response,HttpResponseRedirect
from django.http import HttpResponseRedirect
from django.db.models import Q
from public.publicvar import *
from public.publicfunction import *
from index.models import UserLoginInfo, Logging
from usermanage.models import UserInfo
from projectinfo.models import Project
from review.models import ForReview,ReviewAction
from log.models import LoginLog,ActionLog
from softwaretest.models import SoftwareTest
#from django.template import RequestContext
import commands
import os
import re
import datetime,time
import json
import zipfile
import tarfile

curr_date = time.strftime('%Y-%m-%d %H:%M:%S')#获取当前时间字符串


# ansible_hosts = '/etc/ansible/hosts.bak'        # ansible的hosts文件路径
# # ansible_hosts = '/home/fabu/.ansible/hosts.bak'        # ansible的hosts文件路径
# fabu_yml_path = '/home/fabu/ansible_playbook/fabu.yml '     # 用于升级发布时的playbook文件路径
# newfabu_yml_path = '/home/fabu/ansible_playbook/newfabu.yml '       # 用于全新发布时的playbook文件路径
# ansible-playbook命令
cmd = 'ansible-playbook %s --extra-vars "project_name=%s project_pack=%s project_port=%s backup_time=%s" -f %d -v'

# def read_project_name(section=None):
#     """
#     从hosts文件中获取项目名
#     :param section:项目名。如给定了项目名，则返回该项目的服务器列表
#     :return:列表
#     """
#     # all_project_name = Project.objects.values_list('project_name', 'project_server')
#
#     conf = ConfigParser.ConfigParser()
#     conf.read(ansible_hosts)
#     if section:
#         return conf.options(section)
#     return conf.sections()


def runplaybook(yml_path, project_pack, project_name, project_port, backup_time, num):
    """
    运行ansible-playbook命令
    :param yml_path: playbook脚本(yml文件)路径
    :param project_pack: 压缩包路径
    :param project_name: 项目名
    :param backup_time: 备份文件文件名中的时间
    :param num: 线程数量==项目服务器数量
    :return: 运行状态, output输出
    """
    status, output = commands.getstatusoutput(cmd % (yml_path, project_name, project_pack, project_port, backup_time, num))
#    status, output = commands.getstatusoutput(cmd % (yml_path, project_name, project_pack, project_port, backup_time, 1))
    return status, output

#html转义
def replace_html(s):
    s = s.replace('&quot;','"')
    s = s.replace('&amp;','&')
    s = s.replace('&lt;','<')
    s = s.replace('&gt;','>')
    s = s.replace('&nbsp;',' ')
    # s = s.replace(' - 361way.com','')
    # print s
    return s

def check_ascii(filename_str):
    has_ascii_reg = re.compile(r'[^a-zA-Z0-9\$\@\./_-]')
    has_ascii = has_ascii_reg.findall(filename_str)
    if len(has_ascii) > 0:
        return False
    else:
        return True


def check_pack(pack_path, project_name):
    """
    检测压缩包是否规范，父目录需为 tomcat_项目名
    :param pack_path: 压缩包路径
    :param project_name: 项目模块名
    :return: 布尔
    """
    if pack_path.endswith('.zip'):      # zip包
        try:
            zf = zipfile.ZipFile(pack_path, mode='r')
            filename_lists = zf.filelist
            filename_str = ''.join([i.filename for i in filename_lists])
            has_ascii = check_ascii(filename_str)
            if not has_ascii:
                return '检测到文件名或路径含有非法字符！'
            for i in filename_lists:
                if not i.filename.startswith('tomcat_%s' % project_name):
                    return False
        except IOError:
            return '压缩包读取失败！'
        except UnicodeDecodeError:
        	zf.close()
        	return '检测到文件名或路径含有非法字符！'

    else:
        # 非zip包
        try:
            tf = tarfile.open(pack_path)
            filename_lists = tf.getnames()
            filename_str = ''.join(filename_lists)
            has_ascii = check_ascii(filename_str)
            if not has_ascii:
                return '检测到文件名或路径含有非法字符！'
            for i in filename_lists:
                if not i.startswith('tomcat_%s' % project_name):
                    return False
        except IOError:
            return '压缩包读取失败！'
        except UnicodeDecodeError:
            tf.close()
            return '检测到文件名或路径含有非法字符！'

    return True

def get_client_ip(request):
    try:
      real_ip = request.META['HTTP_X_FORWARDED_FOR']
      regip = real_ip.split(",")[0]
    except:
      try:
        regip = request.META['REMOTE_ADDR']
      except:
        regip = ""
    return regip
def login(request):
    """
    用户登录处理函数
    :param request:
    :return:
    """
    if request.POST:
        LoginName = request.POST['LoginName']       # 获取登录名
        LoginPassword = request.POST['LoginPassword']       # 获取密码

        try:        # 数据库查询
            getUserInfo = UserInfo.objects.get(user=LoginName, password=LoginPassword,user_status='1')
        except UserInfo.DoesNotExist:      # 数据库无对应数据时产生异常则返回错误信息
            return render(request, 'login.html', {'LoginErrMsg': '用户名或密码错误'})

        if getUserInfo:
            # 将用户登录名以及用户的ftp路径写入session
            request.session['LoginName'] = LoginName
            request.session['ftp_path'] = getUserInfo.ftp_path
            # return HttpResponse(get_client_ip(request))
            LoginLog.objects.create(Loginuser=request.session['LoginName'],Logintime=time.strftime('%Y-%m-%d %H:%M:%S'),Logaction=u'登录',LogIP=get_client_ip(request))
            return HttpResponseRedirect('/')
    else:
        request.session.set_expiry(3600*6)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print BASE_DIR
        return render(request, 'login.html')


#判断用户是否登录的装饰器
# def is_login(func):
#     def wrapper(*args,**kwargs):
#         LoginName = request.session['LoginName']
#         try:
#             getUserInfo = UserInfo.objects.get(user=LoginName)
#             have_publish,have_review,have_test = getUserInfo.have_publish,getUserInfo.have_review,getUserInfo.have_test
#         except Exception as e:
#             return render(request, 'login.html')
#         return func(*args,**kwargs)
#     return wrapper

#获取用户权限
def GetUserAuth(user):
	UserObject = UserInfo.objects.get(user=user,user_status='1')
	return UserObject.have_publish,UserObject.have_review,UserObject.have_test

def index(request):
    """
    发布提交页面主处理函数
    :param request:
    :return:
    """
    # LoginName = request.session['LoginName']
    # getUserInfo = UserInfo.objects.get(user=LoginName)
    # have_publish,have_review,have_test = getUserInfo.have_publish,getUserInfo.have_review,getUserInfo.have_test

    if 'LoginName' not in request.session:
        # 用户未登录跳转
        return HttpResponseRedirect('/login/')
    else:
    	have_publish,have_review,have_test = GetUserAuth(request.session['LoginName'])
     	return render(request,'dashboard.html',{'LoginName': request.session['LoginName'],
									     		'navbar':'dashboard',
									     		'url':'/',
									     		'have_publish':have_publish,
									     		'have_review':have_review,
									     		'have_test':have_test})

def LoadNotice(request):
	#获取审核人为登录者并且活跃状态的数据记录数
	ForReviewCount = ForReview.objects.filter(review_owner=request.session['LoginName'],is_active='0').count()
	ForTestCount = SoftwareTest.objects.filter(test_status='0').count()
	data = "{\"ForTestCount\":"+str(ForTestCount)+",\"ForReviewCount\":"+str(ForReviewCount)+"}"
	return HttpResponse(data)


def LoadDisk(request):
    status, output = commands.getstatusoutput('df -h')
    DiskInfo = {}
    for k,v in enumerate(output.split('\n')):
        # print k,v
        # print v.split()[0]
        if k == 0:
            pass
        else:
            DiskInfo[v.split()[0]] = [v.split()[1],v.split()[2],v.split()[4][0:-1],v.split()[5]]

    data = "{\"DiskInfo\":"+json.dumps(DiskInfo)+"}"
    return HttpResponse(data)

def LoadDashboard(request):
    '''
    首页加载数据
    :LastFivePublishLog 最近五条发布日志
    :LastSevenDate 最近七天日期字符串
    '''
    LastFivePublishLog = ReviewAction.objects.values().order_by('-id')[:5]

    '''
    curr_date_str = time.strftime('%Y-%m-%d %H:%M:%S')#获取当前时间字符串
    curr_date = datetime.datetime.strptime(curr_date_str,'%Y-%m-%d %H:%M:%S')#将当前时间转换成可加减的日期格式
    one_mouth_later = curr_date + datetime.timedelta(days=30)
    one_mouth_later_str = one_mouth_later.strftime('%Y-%m-%d %H:%M:%S')
    '''
    LastSevenDate = []
    PublishListUserList = ['fabu01','fabu02','fabu03','fabu04']
    curr_date = datetime.datetime.strptime(time.strftime('%Y-%m-%d'),'%Y-%m-%d')
    for i in range(7):
        LastSevenDate.append((curr_date - datetime.timedelta(days=i)).strftime('%Y-%m-%d'))

    
    # LastSevenDate =['2016-12-21','2016-12-20','2016-12-19','2016-12-18','2016-12-17','2016-12-16','2016-12-15',]

    '''
    新建4*7的二维数组OneWeekPublishCount=[[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
    row代表某个账号，col代表某一天,OneWeekPublishCount[row][col]存储的是发布次数。
    匹配申请日期为LastSevenDate的，且发布人为组列成员的发布总数
    发布总数即是包含所有该发布者发布的总数，包含审批是否通过。
    '''
    OneWeekPublishCount = [[0 for col in range(7)] for row in range(4)]

    for j in range(4):
        for k in range(7):
            OneWeekPublishCount[j][k] = ReviewAction.objects.filter(Q(create_time__contains=LastSevenDate[-(k+1)]),Q(publish_user=PublishListUserList[j])).count()



    '''
    PublishModuleList：所有发布模块组成的列表
    PublishModuleCount：所有发布模块在过去一周内(今天算起过去7天，含今天)的发布次数，与模块名称一一对应
    '''
    PublishModuleList = []
    PublishModuleCount = []
    PublishModuleRejectCount = []

    PublishModuleObj = Project.objects.filter(project_status='1')
    for Module in PublishModuleObj:
        #Module.project_name = '[omweb]'
        PublishModuleList.append(Module.project_name[1:-1])
        PublishModuleCount.append(ReviewAction.objects.filter(Q(review_time__gte=(curr_date - datetime.timedelta(days=6)).strftime('%Y-%m-%d')),Q(publish_module=Module.project_name[1:-1])).filter(publish_status='审核通过,已发布').count())
        PublishModuleRejectCount.append(ReviewAction.objects.filter(Q(review_time__gte=(curr_date - datetime.timedelta(days=6)).strftime('%Y-%m-%d')),Q(publish_module=Module.project_name[1:-1])).filter(publish_status='审核不通过,禁止发布').count())

    # data = "{\"LastFivePublishLog\":"+json.dumps(list(LastFivePublishLog))+",\"LastSevenDate\":"+json.dumps(LastSevenDate)+",\"OneWeekPublishCount\":"+json.dumps(OneWeekPublishCount)+"\
    # ,\"PublishModuleList\":"+json.dumps(PublishModuleList)+",\"PublishModuleCount\":"+json.dumps(PublishModuleCount)+"}"
    data = "{\"LastFivePublishLog\":"+json.dumps(list(LastFivePublishLog))+",\"LastSevenDate\":"+json.dumps(LastSevenDate)+",\"OneWeekPublishCount\":"+json.dumps(OneWeekPublishCount)+"\
    ,\"PublishModuleList\":"+json.dumps(PublishModuleList)+",\"PublishModuleCount\":"+json.dumps(PublishModuleCount)+",\"PublishModuleRejectCount\":"+json.dumps(PublishModuleRejectCount)+"}"
    return HttpResponse(data)





def check_md5(request):
	project_name = request.POST.get('project_name')
	project_pack_md5check = request.POST.get('md5check').lower()
	project_pack = os.path.join(request.session['ftp_path'], request.POST['project_pack'])
	pack_md5 = commands.getoutput("/usr/bin/md5sum %s|awk '{print $1}'" % project_pack)
	publish_code = request.POST.get('publish_code')
	if publish_code == '0':
		# return HttpResponse('全新部署')
		server_list = read_project_name(project_name)
		for i in server_list:
			check_name_status, check_name_output = commands.getstatusoutput("/usr/bin/ssh -p 9055 tomcat@%s 'ls /opt/tomcat_%s'" % (i, project_name))
			if check_name_status != 0:
				return HttpResponse('ModuleIsNoExist')
	# else:
	# 	return HttpResponse('增量部署')
	if project_pack_md5check != pack_md5:
		return HttpResponse('Md5MisMatch')
	else:
		return HttpResponse('Md5Matched')



#发布申请
def Deployment(request):
    if 'LoginName' not in request.session:
        # 用户未登录跳转
        return HttpResponseRedirect('/login/')
    if request.POST:
    	if request.POST['project_name'] == u'=====请选择=====' or request.POST['project_pack'] == u'=====请选择=====':
            return HttpResponse('<h1>项目模块或压缩包未选择！</h1>')

        project_pack = os.path.join(request.session['ftp_path'], request.POST['project_pack'])     # 拼接压缩包完整路径
        project_name = request.POST['project_name']     # 获取前端返回的项目模块名
        # project_pack_md5check = request.POST['md5check'].lower()        # 获取前端返回的md5值，并转换为小写
        runplaybook_state = 'Done'      # runplaybook状态初始化为Done

        reviewer_name = request.POST["reviewer_name"]
        publish_detail = request.POST["publish_detail"]
        publish_type = u'全新部署' if 'newfabu' in request.POST else  u'增量部署'


        # RunPlaybookOutput =[]
        # RunPlaybookOutput.append(runplaybook_state)
        # return render(request, 'result.html', {'RunPlaybookState': RunPlaybookOutput,'LoginName': request.session['LoginName']})
        # return HttpResponseRedirect('/review/')


        '''
        # 检查压缩包打包规范
        check_pack_standard = check_pack(project_pack, project_name)



        if check_pack_standard != True:

            return HttpResponse('<h1>压缩包不规范！</h1>') if check_pack_standard == False \
                else HttpResponse('<h1>%s</h1>' % check_pack_standard)
        '''
        server_list = read_project_name(project_name)       # 获取模块服务器列表

        (the_yml_path, str_fabu) = (newfabu_yml_path, '(全新部署)') if 'newfabu' in request.POST else (fabu_yml_path, '(增量部署)')    # 判断是否为全新发布

        '''
        #验证模块是否存在，已交付check_md5
        if 'newfabu' not in request.POST:

            for i in server_list:
                check_name_status, check_name_output = commands.getstatusoutput("/usr/bin/ssh -p 9055 tomcat@%s 'ls /opt/tomcat_%s'" % (i, project_name))
                if check_name_status != 0:
                    return HttpResponse('<h1>服务器上无此项目模块，请确认是否为全新发布！</h1>')
		
		'''
        # 获取服务器当前时间
        backup_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # return HttpResponse('断点')
        # 获取项目模块端口号
        project_port = Project.objects.get(project_name='[%s]' % project_name).project_port

        #获取文件上传时间
        statinfo=os.stat(project_pack)
        file_uploadtime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(statinfo.st_ctime)))



        # return HttpResponse('断点1')
        #写入待审核数据库
        forreview_dict ={
        'publish_status':u'待审核',
        'publish_type':publish_type,
        'publish_module':project_name,
        'publish_filename':request.POST['project_pack'],
        'publish_user':request.session['LoginName'],
        'file_uploadtime':file_uploadtime,
        'create_time':backup_time,
        'publish_detail':publish_detail,
        'publish_serverlist':server_list,
        'review_owner':reviewer_name,
        }

        #记录发布申请
        ForReview.objects.create(**forreview_dict)
        #记录操作日志
        ActionLog.objects.create(Actionuser=request.session['LoginName'],Actiontime=backup_time,Actiontype=u'发起发布申请',Actionmodule=project_name,Actioninfo=u'文件上传时间:'+file_uploadtime+\
            u';发布类型:'+publish_type+u';发布服务器:'+str(server_list)+u';审核人:'+reviewer_name)
        return HttpResponseRedirect('/review/')
    else:
        request.session.set_expiry(3600*6)
        ftp_path = request.session['ftp_path']      # 获取session中的用户ftp文件夹路径

        dir_list = os.listdir(ftp_path)     # 获取用户ftp文件夹下的文件列表
        file_list = []
        for i in dir_list:
            full_path = os.path.join(ftp_path, i)       # 获取完整文件路径
            if os.path.isfile(full_path) and (full_path.endswith('.tar.gz') or full_path.endswith('.zip') or
                                                  full_path.endswith('.tar') or full_path.endswith('.tgz')):
                # 排除其他文件，只取压缩包
                file_list.append(i)

        project_lists = read_project_name()     # 获取项目名


        Deployment_log = Logging.objects.filter(operation='Deployment').order_by('-ctime')[0:1]

        foradmin = 'block' if request.session['LoginName'] == 'admin' else 'none'
        reviewer_list = []
        reviewer_object = UserInfo.objects.filter(have_review='1',user_status='1')
        for reviewer in reviewer_object:
			reviewer_list.append(reviewer.user)

        # 渲染返回
        # return HttpResponse(project_lists)
        have_publish,have_review,have_test = GetUserAuth(request.session['LoginName'])
        return render(request, 'Deployment.html', {'project_pack': file_list,
                                              'project_lists': project_lists,
                                              'Deployment_log': Deployment_log,
                                              'foradmin': foradmin,
                                              'reviewer_list':reviewer_list,
                                              'LoginName': request.session['LoginName'],
                                              'navbar':'系统发布',
                                              'url':'/Deployment/',
                                              'have_publish':have_publish,
                                              'have_review':have_review,
                                              'have_test':have_test})



def review(request):
    return render(request,'review.html')

def PublishList(request):
    return render(request,'publishlist.html')

#压缩包上传
def fileupload(request):
    if request.method == 'POST':
        fileobj = request.FILES.get('file')
        # filedir = ""
        # for i in UserInfo.objects.get(user=request.session['LoginName']):
        #     filedir = i.ftp_path
        # destination = open(os.path.join('/home/ftp/',request.session['LoginName'],fileobj.name),'wb+')
        destination = open(os.path.join(UserInfo.objects.get(user=request.session['LoginName']).ftp_path,fileobj.name),'wb+')
        for chunk in fileobj.chunks():
            destination.write(chunk)
        destination.close()
        #记录操作日志
        ActionLog.objects.create(Actionuser=request.session['LoginName'],Actiontime=time.strftime('%Y-%m-%d %H:%M:%S'),Actiontype=u'压缩包上传',Actionmodule='-',Actioninfo=u'压缩包名称:'+fileobj.name+\
            u';压缩包完整路径:'+os.path.join(UserInfo.objects.get(user=request.session['LoginName']).ftp_path,fileobj.name))
        return HttpResponse('OK')
        # return True

def GetProjectServerIP(request):

    if 'LoginName' not in request.session:
        # 用户未登录跳转
        return HttpResponseRedirect('/login/')

    elif request.GET['project_name']:
        projectname = request.GET['project_name']
        # return HttpResponse('1')
        projectinfo = Project.objects.get(project_name='[%s]' % projectname)
        result = {'project_name': projectinfo.project_name.strip('[]'),
                  'project_server': projectinfo.project_server.replace(',', '</br>').replace(':9055', ''),
                  'project_port': projectinfo.project_port}
        return HttpResponse(json.dumps(result))


def GetReviewer(request):
	'''
	获取审核人
	'''
	if 'LoginName' not in request.session:
		return HttpResponseRedirect('/login/')
	else:
		reviewer_object = UserInfo.objects.filter(have_review='1',user_status='1')

		reviewer_list ={}
		for reviewer in reviewer_object:
			reviewer_list[reviewer.user]=reviewer.user
		# 	reviewer_list.append(reviewer.user)

		data = "{\"reviewer_list\":"+json.dumps(list(reviewer_list))+"}"
		return HttpResponse(data)


def logout(request):
    from django.contrib.auth import logout
    LoginLog.objects.create(Loginuser=request.session['LoginName'],Logouttime=time.strftime('%Y-%m-%d %H:%M:%S'),Logaction=u'<span class="red">注销</spa>',LogIP=get_client_ip(request))
    logout(request)
    # LoginLog.objects.create(Loginuser=request.session['LoginName'],Logintime=curr_date,Logaction=u'注销')
    return HttpResponseRedirect('/login/')


# def rollback(request):
#     if 'LoginName' not in request.session:
#         # 用户未登录跳转
#         return HttpResponseRedirect('/login/')
#     if request.POST:
#         # 操作提交
#         pass
#     else:
#         return render(request, 'rollback.html', {'project_lists': read_project_name()})


def test(request):
    have_publish,have_review,have_test = GetUserAuth(request.session['LoginName'])
    return render(request,'404.html',{'LoginName': request.session['LoginName'],
                                                'navbar':'error',
                                                'url':'/',
                                                'have_publish':have_publish,
                                                'have_review':have_review,
                                                'have_test':have_test})

