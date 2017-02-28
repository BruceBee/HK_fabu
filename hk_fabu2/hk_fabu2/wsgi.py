import os
from os.path import join,dirname,abspath
from django.core.wsgi import get_wsgi_application
 
PROJECT_DIR = dirname(dirname(abspath(__file__)))#3
import sys # 4
sys.path.insert(0,PROJECT_DIR) # 5
 
os.environ["DJANGO_SETTINGS_MODULE"] = "hk_fabu2.settings" # 7
 
# from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
