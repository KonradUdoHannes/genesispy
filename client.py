from config import settings
import requests
from lxml import etree
from io import StringIO

WADL_NAMESPACE = {'t': 'http://wadl.dev.java.net/2009/02'}

class GenesisClient():
    def __init__(self):
        resp = requests.get(settings.url.wadl)
        self._wadl_tree = etree.fromstring(bytes(resp.text,encoding='UTF8'))
        
    def api_info(self,path=None):
        """Returns information about the API at path.
        
        Path can either be None/an empty list, a list with one element or with two.
        For 0/1 element lists. The function returns the endpoint hirarchy below
        this value. For a two element list information about the particular endpoint
        is returned, specifically about its possible parameters. For convenience
        4 parameters have been singled out in the (auth/page/language) output.
        auth: True -> parameters username and password are present (both have default "GAST")
        page: True -> parameter pagelength is present (default 100)
        laguage: True -> parameter language is present (default = 'de')
        """ 
        return endpoint_overview(path,self._wadl_tree) 
    
    @staticmethod
    def _is_file_endpoint(path):
        if len(path) != 2:
            raise ValueError('Endpoint paths need to contain two elements')
        return "file" in path[-1] or "chart" in path[-1] or "map" in path[-1]
    
    def get_json(self,path,params=None):
        """Query API Endpoints that return json.
        """
        if self._is_file_endpoint(path):
            raise ValueError('Not suited for file/chart/map endpoints. Use get_file.')
        return send_request(path,self._wadl_tree,params).json()
    
    def get_file(self,path,filename,params=None):
        """Query API Endpoints that return a file.
        """
        if not self._is_file_endpoint(path):
            raise ValueError('Only suited for file/chart/map endpoints. Use get_json.')
        content = send_request(path,self._wadl_tree,params)
        with open(filename,'bw') as f:
             f.write(content.content)
        

def endpoint_overview(path,wadl_tree):
    namespaces= WADL_NAMESPACE
    if path is None:
        path = []
    if len(path) == 0:
        xpath = "/t:application/t:resources/t:resource/@path"
    elif len(path) == 1:
        xpath = f"/t:application/t:resources/t:resource[@path='/{path[0]}']/t:resource/@path"
    elif len(path) == 2:
        xpath = f"/t:application/t:resources/t:resource[@path='/{path[0]}']/t:resource[@path='/{path[1]}']/t:method"
        method = wadl_tree.xpath(xpath,namespaces=namespaces)
        if len(method) > 0:
            params = [x.attrib for x in method[0].getchildren()[0].getchildren()]
            usr = [d for d in params if d['name'] == 'username']
            pwd = [d for d in params if d['name'] == 'password']
            page = [d for d in params if d['name'] == 'pagelength']
            lan = [d for d in params if d['name'] == 'language']
            excl_list = ['username','password','pagelength','language']
            
            return {
                'id' : method[0].attrib['id'],
                'method' : method[0].attrib['name'],
                'auth/page/language' : (len(usr)==1 & len(pwd)==1,len(page)==1,len(lan)==1),
                'params' : [p for p in params if p['name'] not in excl_list]
            }
        
    return [endpoint.strip('/') for endpoint in wadl_tree.xpath(xpath,namespaces=namespaces)]

def send_request(path,wadl_tree,params = None):
    namespaces= WADL_NAMESPACE
    if len(path) != 2:
        raise ValueError("Path needs length 2")
    if params is None:
        params = {}
    base_url = wadl_tree.xpath("/t:application/t:resources/@base",namespaces=namespaces)[0]
    endpoint = f"{base_url}/{path[0]}/{path[1]}"
    info = endpoint_overview(path,wadl_tree)
    if info['auth/page/language'][0]:
        if 'username' not in params:
            params['username'] = settings.get('genesis_usr','GAST')
        if 'password' not in params:
            params['password'] = settings.get('genesis_pwd','GAST')
        
    query_string = "?" + '&'.join([f"{key}={value}" for key,value in params.items()])
    url = endpoint + query_string
    resp = requests.get(url)
    assert resp.status_code == 200, f"Got status_code: {resp.status_code} for {url}"
    return resp