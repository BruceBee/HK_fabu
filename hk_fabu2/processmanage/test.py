# -*- coding:utf-8 -*-

import json
import os,sys
import commands
import time
import django


BASE_DIR=os.path.dirname(os.getcwd())
print os.getcwd()
sys.path.append(BASE_DIR+'/fabu/hk_fabu2')
sys.path.append('/home/fabu/hk_fabu2')
# import hk_fabu2
print sys.path
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hk_fabu2.settings")
django.setup()
from processmanage.models import ProcessInfo



