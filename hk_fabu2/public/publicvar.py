#!/usr/bin/env python
# -*- coding:utf-8 -*-


#ansible_hosts = '/etc/ansible/hosts.bak'        # ansible的hosts文件路径
ansible_hosts = '/home/fabu/.ansible/hosts'        # ansible的hosts文件路径
ansible_playbook_path = '/home/fabu/ansible_playbook'
fabu_yml_path = ansible_playbook_path + '/' + 'fabu.yml '     # 用于升级发布时的playbook文件路径
newfabu_yml_path = ansible_playbook_path + '/' + 'newfabu.yml '       # 用于全新发布时的playbook文件路径
operation_yml_path = ansible_playbook_path + '/' + 'startstoprestart.yml'
the_ssh_port = 9055
TOMCAT_LOG_PATH_MOUNT = '/tomcat_logs'
System_Excute_User = 'fabu'
