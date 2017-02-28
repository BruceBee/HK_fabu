import os
from os.path import join,dirname,abspath
 
PROJECT_DIR = dirname(dirname(abspath(__file__)))
print PROJECT_DIR
import sys
sys.path.insert(0,PROJECT_DIR) # 5
 
os.environ["DJANGO_SETTINGS_MODULE"] = "hk_fabu2.settings"
 
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
