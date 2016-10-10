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
from controllers.customers_drop_down_service import Rma_customer_dropdown
class Root(object):
    rma_customer_dropdown_service = Rma_customer_dropdown()
    @cherrypy.expose
    def index(self, term=None):
        r = redis.StrictRedis(host='localhost', port=6379, db=REDIS_DB)

        engine = tenjin.Engine(path=['views'])
        ## context data
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
                if re.search(pattern, vobj['customer_name'], re.IGNORECASE) or \
                        re.search(pattern, vobj['site_name'], re.IGNORECASE):
                    for r in vobj['returns']:
                        customers_result.append(
                            {
                                 'id':r['id'],
                                 'ts':r['ts'],
                                 'date':r['date'],
                                 'customer_name': vobj['customer_name'],
                                 'site_name': vobj['site_name'],
                                 'url': r['url'],
                                 'share_point_url': r['share_point_url'],
                                 'issue': r['issue'],
                                 'case_number': r['case_number']
                            }
                        )
            customers_sorted = sorted(customers_result, key=itemgetter('ts'), reverse=True)
            context = {
                'keys': customers_sorted
            }
        else:
            context = {
                'keys': [],
            }
        ## render template with context data

        html = engine.render('page.pyhtml', context)
        return html

if __name__ == '__main__':
    cherrypy.config.update({
        'server.socket_port': CHERRYPY_PORT,
        'tools.proxy.on': True,
        'tools.proxy.base': SITE_BASE
    })

    cherrypy.quickstart(Root(), SITE_URI)
