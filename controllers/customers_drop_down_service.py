import cherrypy
import tenjin
from settings import SITE_URI
from settings import SITE_BASE
from settings import CHERRYPY_PORT

from settings import REDIS_DB
from tenjin.helpers import *
import redis
import json
import re
from url_decode import urldecode
from operator import itemgetter
class Rma_customer_dropdown(object):
    @cherrypy.expose
    def index(self, term=None):
        #return '{"customers": [{"id":"123", "name": "hi!"}]}'
        r = redis.StrictRedis(host='localhost', port=6379, db=REDIS_DB)

        ## context data
        customers_sorted = []
        if term:
            customers_result = []
            keys = r.keys('*')

            if len(keys) > 0:
                vals = r.mget(keys)
            else:
                vals = []

            for v in vals:
                vobj = json.loads(v)
                pattern = '[A-Za-z0-9]*%s'%urldecode(term)
                if re.search(pattern, vobj['customer_name'], re.IGNORECASE):
                    obj = {
                         'id': vobj['id'],
                         'name': vobj['customer_name'],
                        }

                    # correcting upstream defect with multiple records
                    # we are cycling through the list of sites to get customers
                    # producting redundant hits.
                    if obj not in customers_result:
                        customers_result.append(obj)
            customers_sorted = sorted(customers_result, key=itemgetter('name'))

        result = {"customers": customers_sorted}
        ## render template with context data
        return json.dumps(result)