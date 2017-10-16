import requests
from requests.auth import HTTPBasicAuth
import csv
import codecs
from unidecode import unidecode

DATA_DIR= 'C:/work/web/BIlboards-data/nubium/'

def picture(id, mesto, type):
    try:
    #resp = requests.get('http://www.ponuka.nubium.sk/rp/nahlady-s/trnava/12-3-1-1-13.jpg',
        resp = requests.get('http://www.ponuka.nubium.sk/rp/{0}/{1}/{2}.jpg'.format(type, mesto, id),
             auth=HTTPBasicAuth('nubium', 'objednat'))
             #cookies = auth)
        if resp.ok and resp.headers['Content-Type'] == 'image/jpeg':
            with open(DATA_DIR+type+'/'+id+'.jpg', 'wb') as ff:
                ff.write(resp.content)
            return True
        else:
            return False
    except:
        return False
