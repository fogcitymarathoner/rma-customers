"""
"""
__author__ = 'marc'
from fabric.api import run
from fabric.api import local
from datetime import datetime as dt
#SERVER_NAME='crm1.corp.enlightedinc.com' # crm1.corp.enlightedinc.com
SERVER_NAME='fogtest.com'
#SERVER_USER='crm' # crm1.corp.enlightedinc.com
SERVER_USER='marc' # fogtest.com
#DEST='python_apps/cherrypy/customers_test/' # crm1.corp.enlightedinc.com
DEST='python_test_apps/rma_customers' # fogtest.com
def sync():
	"""
	sync with 10.8.3.10 test directory
	"""
	local('rsync -arv --delete --exclude ".git" --exclude "static" ./* %s@%s:%s'%
          (SERVER_USER, SERVER_NAME, DEST))
