#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse
from django.db.models import Q
from projectinfo.models import Project,Server
# from index.models import Logging
from log.models import ActionLog
# from index.models import UserLoginInfo
from public.publicvar import *
from public.publicfunction import *
import StringIO
import ConfigParser
import re
import json
import time
import commands


#the_ssh_port = 9055     # 服务器默认SSH端口，会统一加到ansible的hosts文件中
#ansible_hosts = '/home/fabu/.ansible/hosts'        # ansible的hosts文件路径

re_find_project_name = re.compile(r'^\[[0-9a-zA-Z_]{,30}\]:.*')       # 允许的项目名

# ipv4地址的正则匹配
re_ipv4 = re.compile(r'^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
                     r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
                     r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
                     r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
re_remark = re.compile(r'^#.*$')        # 注释文本的正则匹配


class ProjectInfoInputError(Exception):
    """
    自定义异常类，于检测到前端输入错误时引发异常
    """
    def __init__(self, x):
        Exception.__init__(self, x)
        self.x = x


def _add_port(x, port):
    """
    为项目列表的ip添加端口
    :param x: 项目列表：[{’项目名1‘：{'ip':[ip列表],'msg':'注释文本信息'}},{’项目名2‘：{'ip':[ip列表],'msg':'注释文本信息'}}]
    :param port: 服务器默认SSH端口
    :return: 添加端口后的项目列表
    """
    add_del = x
    for i, v in enumerate(add_del):
        for a in range(len(add_del[i][v.keys()[0]]['ip'])):
            add_del[i][v.keys()[0]]['ip'][a] = add_del[i][v.keys()[0]]['ip'][a] + ':%s' % str(port)
    return add_del

#获取服务组成的列表
def getserverlist(request):
    
    ServerList = Server.objects.values('server_name','server_ip').order_by('server_ip')
    ModuleList = Project.objects.values('project_name','project_server').order_by('project_name')
    

    # data = "{\"ServerList\":"+json.dumps(list(ServerList))+"}"

    # data = "{\"LastFivePublishLog\":"+json.dumps(list(LastFivePublishLog))+",\"LastSevenDate\":"+json.dumps(LastSevenDate)+",\"OneWeekPublishCount\":"+json.dumps(OneWeekPublishCount)+"\
    # ,\"PublishModuleList\":"+json.dumps(PublishModuleList)+",\"PublishModuleCount\":"+json.dumps(PublishModuleCount)+",\"PublishModuleRejectCount\":"+json.dumps(PublishModuleRejectCount)+"}"
    
    data = "{\"ServerList\":"+json.dumps(list(ServerList))+",\"ModuleList\":"+json.dumps(list(ModuleList))+"}"
    

    return HttpResponse(data)
    
def projectinfo(request):
    """
    /projectinfo/页面处理函数
    :param request:
    :return:
    """
    if 'LoginName' not in request.session:
        # 检查是否登录
        return HttpResponseRedirect('/login/')
    if request.session['LoginName'] != 'admin':
        return HttpResponseRedirect('/')
    if request.POST:
        # 页面POST返回数据处理
        try:
            # 检测POST过来的项目信息格式，检测过程遇到非法格式则触发自定义异常

            # 去除整段项目信息文本的段前段后空白，并按行拆分为列表
            projectinfo_input_list = request.POST['projectinfo'].strip().split('\n')
            # 去除列表各项文本的行前行后空白
            projectinfo_input_list = map(lambda x: x.strip(), [i for i in projectinfo_input_list])
            project_lists = []

            if not re_find_project_name.match(projectinfo_input_list[0]):
                # 首先非[项目名]开始则异常
                raise ProjectInfoInputError('输入格式有误！')

            for i, v in enumerate(projectinfo_input_list):
                # 项目信息检测主逻辑

                # project_dict = {}       # 单个项目

                if re.match(r'^$', v):
                    # 跳过空行
                    continue

                if v.endswith(']') or v.endswith(':'):
                    raise ProjectInfoInputError('似乎有端口忘了输入！')

                if re_find_project_name.match(v):
                    # 检测到[项目名]则进入for
                    project_ip = []
                    project_msg = ''
                    # 项目名格式查错，分离项目名与项目端口
                    project_name_port = v.split(':')
                    if len(project_name_port) != 2:
                        raise ProjectInfoInputError('输入格式有误！')

                    if project_name_port[1].isnumeric():
                        if 80 <= int(project_name_port[1]) <= 65535:
                            project_port = project_name_port[1]
                        else:
                            raise ProjectInfoInputError('端口范围必须为80-65535！')
                    else:
                        raise ProjectInfoInputError('输入格式有误！')

                    v = project_name_port[0]

                    # if not 10 <= int(project_port) <= 65535:
                    #     # 检查项目端口是否正确
                    #     raise ProjectInfoInputError('端口输入有误！')

                    for k in projectinfo_input_list[i + 1:]:
                        # 检索[项目名]后面的内容

                        if re.match(r'^$', k):
                            # 跳过空行
                            continue

                        if re_find_project_name.match(k):
                            # 如果再次检测到[项目名]则跳出项目内容检索
                            break

                        if re_remark.match(k):
                            # 检索到注释
                            project_msg = project_msg + re_remark.match(k).group(0)

                        if re_ipv4.match(k):
                            # 检索到ipv4地址
                            project_ip.append(k)

                    project_dict = dict([(v, dict([
                        ('msg', project_msg),
                        ('ip', project_ip),
                        ('project_port', project_port)
                    ]))])

                    if len(project_dict[v]['ip']) >= 1:
                        # ipv4地址列表存在则视为有效信息并添加到project_lists列表
                        project_lists.append(project_dict)

            # 检查项目端口是否有重复
            all_project_port = [each.values()[0]['project_port'] for each in project_lists]
            if len(set(all_project_port)) != len(all_project_port):
                raise ProjectInfoInputError('有重复的端口！')

            add_port = _add_port(project_lists, port=the_ssh_port)       # 为IP地址添加端口

            write_line = []
            # 将项目信息转换为列表以便写入hosts文件
            for i in add_port:
                write_line.append(i.keys()[0] if not write_line else '\n' + i.keys()[0])
                write_line.append(i.values()[0]['msg'])
                write_line.append('\n'.join(i.values()[0]['ip']))

            # 利用StringIO模块将项目信息存为内存文件以便使用ConfigParser进行最后检测
            f = StringIO.StringIO()
            f.write('\n'.join(write_line))
            f.seek(0)

            try:        # 使用ConfigParser进行最后检测
                conf = ConfigParser.ConfigParser()
                conf.readfp(f)
            except ConfigParser.Error:      # ConfigParser模块异常则触发自定义异常
                raise ProjectInfoInputError('难以发现的格式错误！')

            try:        # 写入hosts文件
                f.seek(0)       # 指针回位
                with open(ansible_hosts, 'w') as hosts:
                    hosts.write(f.read().encode("UTF-8"))
            except IOError:
                raise ProjectInfoInputError('ansible hosts文件写入失败')

            for i in project_lists:
                try:        # 数据库写入
                    w_db = dict([
                        ('project_name', i.keys()[0]),
                        ('project_msg', i.values()[0]['msg']),
                        ('project_server', ','.join(i.values()[0]['ip'])),
                        ('project_port', int(i.values()[0]['project_port']))
                    ])

                    # 项目信息更新或新建
                    Project.objects.update_or_create(project_name=w_db['project_name'], defaults=w_db)

                    # 日志写入
                    w_logging = Logging(state='Done', user=request.session['LoginName'],
                                        project_name=w_db['project_name'], dest_server=w_db['project_server'],
                                        log_date=w_db['project_msg'], operation='ModefyProject')
                    w_logging.save()

                except:
                    raise ProjectInfoInputError('数据库写入失败！')

            try:        # 删除多余的项目
                # 获取数据库中所有项目名称
                all_project_indb = Project.objects.values_list('project_name')

                # 获取多余的项目名
                del_project = list(set(x[0] for x in all_project_indb) - set([x.keys()[0] for x in project_lists]))

                # 删除多余项目
                map(lambda x: Project.objects.get(project_name=x).delete(), del_project)

                # 删除项目-日志写入
                map(lambda x: Logging.objects.create(user=request.session['LoginName'],
                                                     project_name=x, state='Done',
                                                     dest_server='DELETE',
                                                     log_date='DELETE',
                                                     operation='ModefyProject'), del_project)

            except:
                raise ProjectInfoInputError('数据库写入失败！')

            f.close()       # 内存文件关闭

        except ProjectInfoInputError, e:
            return render(request, 'projectinfo/projectinfo.html', {'ProjectInfoInputError': e,
                                                        'projectinfo': projectinfo_input_list})

        # return HttpResponse('<h1>操作成功</h1><br /><a href="">返回</a>')
        return render(request,'projectinfo/result.html',{'status':'Done','LoginName': request.session['LoginName']})
    else:
        # GET页面请求
        all_project = Project.objects.all()     # 获取数据库所有项目
        projectinfo_input_list = []
        for each_project_obj in all_project:
            # 以 项目名 项目注释 项目IP列表 为次序，顺序添加进projectinfo_input_list列表

            # 如果不是第一个项目则在项目名前添加换行，利于前端页面的展示
            send_project_name = each_project_obj.project_name + ':' + str(each_project_obj.project_port)
            projectinfo_input_list.append(send_project_name if not projectinfo_input_list else '\n' + send_project_name)
            # 添加注释
            projectinfo_input_list.append(each_project_obj.project_msg.replace('#', '\n#').strip())
            # 遍历项目IP并按顺序添加
            for i in each_project_obj.project_server.split(','):
                projectinfo_input_list.append(i.split(':')[0])
        # 渲染返回
        have_publish,have_review,have_test = GetUserAuth(request.session['LoginName'])
        return render(request, 'projectinfo/projectinfo.html', {'projectinfo': projectinfo_input_list,
                                                                'LoginName': request.session['LoginName'],
                                                                'navbar':'项目模块管理',
                                                                'url':'/projectinfo/',
                                                                'have_publish':have_publish,
                                                                'have_review':have_review,
                                                                'have_test':have_test})

#返回服务器查询内容(全量态+查询态)
def GetServerInfoList(request):
    try:
        '''
        返回服务器配置列表
        '''
        k_words = request.POST.get('k_words','').encode('utf-8')
        s_page = request.POST.get('s_page','')
        # e_page = request.POST.get('e_page','')
        page_size = request.POST.get('page_size','')
        # if request.method  == 'GET':
        # ProjectInfo_obj = Project.objects.values().order_by('-id')[(int(s_page)-1)*int(page_size):int(s_page)*int(page_size)]
        
        # Server_obj = Server.objects.values().order_by('-id')[(int(s_page)-1)*int(page_size):int(s_page)*int(page_size)]
        # data = "{\"Server_data\":"+json.dumps(list(Server_obj))+"}"

        Server_obj = Server.objects.filter(Q(server_name__contains=str(k_words)) \
            | Q(server_ip__contains=str(k_words)) \
            | Q(ssh_port__contains=str(k_words)) \
            | Q(server_remark__contains=str(k_words))).values().order_by('-server_name')[(int(s_page)-1)*int(page_size):int(s_page)*int(page_size)]
        data = "{\"Server_data\":"+json.dumps(list(Server_obj))+"}"
        if k_words != "":
            ActionLog.objects.create(Actionuser=request.session['LoginName'],\
                                     Actiontime=time.strftime('%Y-%m-%d %H:%M:%S'),\
                                     Actiontype=u'服务器数据查询',\
                                     Actionmodule='-',\
                                     Actioninfo=u'查询内容:'+request.POST.get('k_words',''))


        return HttpResponse(data)
    except Exception as e:
        return HttpResponse('302')

def GetServerInfoCount(request):
    try:
        #返回模块配置列表总记录数
        # page_total = Server.objects.all().count()
        k_words = request.POST.get('k_words','').encode('utf-8')
        page_total = Server.objects.filter(Q(server_name__contains=str(k_words)) \
            | Q(server_ip__contains=str(k_words)) \
            | Q(ssh_port__contains=str(k_words)) \
            | Q(server_remark__contains=str(k_words))).count()
        return HttpResponse(page_total)
    except Exception as e:
        return HttpResponse('303')

#返回模块查询内容(全量态+查询态)
def GetModuleInfoList(request):
    try:
        '''
        返回查询模块配置列表
        '''
        k_words = request.POST.get('k_words','').encode('utf-8')
        # return HttpResponse(k_words)
        s_page = request.POST.get('s_page','')
        # e_page = request.POST.get('e_page','')
        page_size = request.POST.get('page_size','')
        # if request.method  == 'GET':
        # ProjectInfo_obj = Project.objects.values().order_by('-id')[(int(s_page)-1)*int(page_size):int(s_page)*int(page_size)]
        # ProjectInfo_obj = Project.objects.filter(project_name='[ucweb]').values()
        ProjectInfo_obj = Project.objects.filter(Q(project_name__contains=str(k_words)) \
            | Q(project_server__contains=str(k_words)) \
            | Q(project_msg__contains=str(k_words)) \
            | Q(project_port__contains=str(k_words))).values().order_by('-project_name')[(int(s_page)-1)*int(page_size):int(s_page)*int(page_size)]
        data = "{\"ProjectInfo_data\":"+json.dumps(list(ProjectInfo_obj))+"}"
        if k_words != "":
            ActionLog.objects.create(Actionuser=request.session['LoginName'],\
                                     Actiontime=time.strftime('%Y-%m-%d %H:%M:%S'),\
                                     Actiontype=u'模块数据查询',\
                                     Actionmodule='-',\
                                     Actioninfo=u'查询内容:'+request.POST.get('k_words',''))

        return HttpResponse(data)
    except Exception as e:
        return HttpResponse(e)

def GetModuleInfoCount(request):
    try:
        #返回查询模块配置列表总记录数
        k_words = request.POST.get('k_words','').encode('utf-8')
        page_total = Project.objects.filter(Q(project_name__contains=str(k_words)) \
            | Q(project_server__contains=str(k_words)) \
            | Q(project_msg__contains=str(k_words)) \
            | Q(project_port__contains=str(k_words))).count()
        return HttpResponse(page_total)
    except Exception as e:
        return HttpResponse('303')


def GetProjectInfoList(request):
    try:
        '''
        返回模块配置列表
        '''
        s_page = request.POST.get('s_page','')
        # e_page = request.POST.get('e_page','')
        page_size = request.POST.get('page_size','')
        # if request.method  == 'GET':
        # ProjectInfo_obj = Project.objects.values().order_by('-id')[(int(s_page)-1)*int(page_size):int(s_page)*int(page_size)]
        

        # ProjectInfo_obj = Project.objects.values().order_by('-project_name')[(int(s_page)-1)*int(page_size):int(s_page)*int(page_size)]
        # data = "{\"ProjectInfo_data\":"+json.dumps(list(ProjectInfo_obj))+"}"



        ProjectInfo_obj = Project.objects.values().order_by('-project_name')[(int(s_page)-1)*int(page_size):int(s_page)*int(page_size)]
        data = "{\"ProjectInfo_data\":"+json.dumps(list(ProjectInfo_obj))+"}"





        return HttpResponse(data)
    except Exception as e:
        return HttpResponse('302')

def GetProjectInfoCount(request):
    try:
        #返回模块配置列表总记录数
        page_total = Project.objects.all().count()
        return HttpResponse(page_total)
    except Exception as e:
        return HttpResponse('303')


def project_check(request):
    modulename = request.POST.get('modulename','')
    moduleport = request.POST.get('moduleport','')

    if Project.objects.filter(project_name=modulename).count() > 0:
        return '模块名已存在'
    if Project.objects.filter(project_port=moduleport).count() > 0:
        return '端口已存在'


def addserver(request):
    try:
        servername = request.POST.get('servername','')
        serverip = request.POST.get('serverip','')
        sshport = request.POST.get('sshport','')
        loginpasswd = request.POST.get('loginpasswd','')
        serverremark = request.POST.get('serverremark','')

        # return HttpResponse('1')
        # aa =  Server.objects.filter(server_name = servername).count()
        # return HttpResponse(aa)
        if Server.objects.filter(server_name = servername.strip()).count() != 0:
            return HttpResponse('ServerNameExist')
        if Server.objects.filter(server_ip = serverip.strip()).count() != 0:
            return HttpResponse('ServerIpExist')

        
        #建立宿主机与该客户端服务器的免密钥认证
        status, output = commands.getstatusoutput('/home/fabu/hk_fabu2/bulidcertification.sh %s %s %s ' % (serverip,sshport,loginpasswd))
        # return HttpResponse(status)
        if status != 0:
            return HttpResponse(output)
        else:
            #写入Ansible hosts文件
            try:
                with open(ansible_hosts, 'a+') as hosts:
                    hosts.write('\n#'+serverremark+'\n'+serverip+':'+sshport+'\n')
            except IOError:
                raise ProjectInfoInputError('ansible hosts文件写入失败')
            # 服务器信息新建
            Server.objects.create(server_name=servername,\
                     server_ip=serverip,\
                     ssh_port=sshport,\
                     root_passwd=loginpasswd,\
                     server_remark=serverremark,\
                     create_time=time.strftime('%Y-%m-%d %H:%M:%S'),\
                     create_user=request.session['LoginName'],\
                     server_status='1')
            #记录操作日志
            ActionLog.objects.create(Actionuser=request.session['LoginName'],Actiontime=time.strftime('%Y-%m-%d %H:%M:%S'),Actiontype=u'新建服务器',Actionmodule='-',Actioninfo=u'服务器名称:'+servername+\
                    u';服务器IP:'+serverip+u';服务器SSH端口:'+sshport+u';服务器备注:'+serverremark)

            return HttpResponse('addsuccess')
    except Exception as e:
        return HttpResponse('addfaild')


def addmodule(request):
    modulename = request.POST.get('modulename','')
    moduleremark = request.POST.get('moduleremark','')
    moduleport = request.POST.get('moduleport','')
    moduleserverlist = request.POST.get('moduleserverlist','')

    if Project.objects.filter(project_name='['+modulename+']').count() > 0:
        return HttpResponse('1')
    if not moduleport.isdigit() or Project.objects.filter(project_port=moduleport).count() > 0:
        return HttpResponse('2')

    server_list = []
    for i in range(len(moduleserverlist.split(';'))-1):
        if re_ipv4.match(moduleserverlist.split(';')[i]):
            # 检索到ipv4地址
            server_list.append(moduleserverlist.split(';')[i])
        else:
            return HttpResponse('3')
        # server_list.append(moduleserverlist.split(';')[i])
    
    
    try:
        # 写入hosts文件
        with open(ansible_hosts, 'a+') as hosts:
            hosts.write('\n['+modulename+']\n'+'#'+modulename+'\n')
            for j in range(len(server_list)):
                hosts.write(server_list[j]+':'+'9055'+'\n')

            # hosts.write('\n['+modulename+']\n'+'#'+modulename+'\n'+'192.168.0.1'+':'+'9055'+'\n\n')
            # 项目信息更新或新建
            Project.objects.create(project_name='['+modulename+']',\
             project_server=moduleserverlist,\
             project_msg='#'+moduleremark,\
             project_port=moduleport,\
             create_user=request.session['LoginName'],\
             create_time=time.strftime('%Y-%m-%d %H:%M:%S'),\
             project_status='1'
                )
            #记录操作日志
            ActionLog.objects.create(Actionuser=request.session['LoginName'],Actiontime=time.strftime('%Y-%m-%d %H:%M:%S'),Actiontype=u'新建项目模块',Actionmodule='-',Actioninfo=u'模块名称:'+modulename+\
            u';模块端口:'+moduleport+u';模块备注:'+moduleremark+u';下属服务器:'+moduleserverlist)
    except IOError:
        raise ProjectInfoInputError('ansible hosts文件写入失败')
    

    return HttpResponse('4')


#模块信息修改，如果模块名发生变更，即等同于创建
def projectupdate(request):
    return HttpResponse('1')


def UpadteHostsFile(module,status,servercount):
    #执行写入hosts文件函数
    with open(ansible_hosts, 'r') as hosts:
        hostslist = hosts.readlines()
    '''
    模块状态status
    0-停用模块：即需要将当前启用状态转变成注释状态，应该以非#开头字符串进行匹配
    1-启用模块，注释转启用，即以注释状态字符串进行匹配
    '''

    if status == '0':
        module = '['+module+']\n'
    else:module = '#['+module+']\n'

    #取出匹配的项
    for index in range(len(hostslist)):
        #module = omweb
        #hostslist[index] = [omweb]
        if module == hostslist[index]:
            for i in range(servercount+2):
                #增加/剔除注释符号
                if status == '0':
                    hostslist[index+i] = '#'+hostslist[index+i]
                else:hostslist[index+i] = hostslist[index+i][1:]

    #重新写入文件
    with open(ansible_hosts, 'w') as hosts:
        hosts.writelines(hostslist)

    return True

def projectswitch(request):
    modulename = request.POST.get('modulename','')
    moduleaction = request.POST.get('moduleaction','')
    serverlist = request.POST.get('serverlist','')
    # return HttpResponse(moduleaction)
    #获取下属服务器数量
    servercount = len(serverlist.split(';'))-1
    '''
    获取模块状态标识project_status：
    0-停用模块
    1-启用模块
    '''
    project_status = '1' if moduleaction == '1' else '0'

    if UpadteHostsFile(modulename,project_status,servercount):
        Project.objects.filter(project_name='['+modulename+']').update(project_status=project_status,update_time=time.strftime('%Y-%m-%d %H:%M:%S'),update_user=request.session['LoginName'])
        #记录操作日志
        ActionLog.objects.create(Actionuser=request.session['LoginName'],\
            Actiontime=time.strftime('%Y-%m-%d %H:%M:%S'),\
            Actiontype=u'模块状态切换',\
            Actionmodule=modulename,\
            Actioninfo=u'模块名称:'+modulename+u'&nbsp;模块当前状态:'+project_status+u';&nbsp;(0-已停用;1-已启用)')
        return HttpResponse('switched')
    else:
        return HttpResponse('error:miss switched')
        
#服务器详情
def serverinfo(request,args):
    have_publish,have_review,have_test = GetUserAuth(request.session['LoginName'])
    serverobj = Server.objects.get(server_name=args)
    return render(request,'projectinfo/serverinfo.html',{'servername': args,
                                                         'LoginName': request.session['LoginName'],
                                                         'navbar':'项目模块管理',
                                                         'url':'/projectinfo/',
                                                         'have_publish':have_publish,
                                                         'have_review':have_review,
                                                         'have_test':have_test,
                                                         'remark':serverobj.server_remark})

#获取同步数据
def rsynserverinfo(request):
    serverip = request.POST.get('serverip','')
    # return HttpResponse(serverip)
    ip = Server.objects.get(server_ip=serverip)
    status, output = commands.getstatusoutput('ansible %s -m setup' % ip.server_ip)
    param = json.loads(output.split('SUCCESS => ')[1])

    print param['ansible_facts']['ansible_distribution']
    return HttpResponse(output.split('SUCCESS => ')[1].split('\n'))

#获取指定服务器已运行时间
def uptime(request):
    serverip = request.POST.get('serverip','')
    ip = Server.objects.get(server_ip=serverip)
    status, output = commands.getstatusoutput("ansible %s -a 'uptime'" % ip.server_ip)
    return HttpResponse(output.split('\n')[1].split('up')[1].split('load')[0])
