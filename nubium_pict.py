import requests
from requests.auth import HTTPBasicAuth
import csv
import codecs
from unidecode import unidecode

DATA_FILE = 'C:/work/web/BIlboards-data/nubium/Nubium-ponuka-1765525-vsetky.csv'
DATA_DIR= 'C:/work/web/BIlboards-data/nubium/'
ERR_FILE = open('err.csv', 'wb')
err_writer = csv.writer(ERR_FILE, delimiter=';')

def login():
    resp = requests.get('http://www.ponuka.nubium.sk/1765525',
        auth=HTTPBasicAuth('nubium', 'objednat'))
    return resp.cookies

def picture(id, mesto, type):
    #resp = requests.get('http://www.ponuka.nubium.sk/rp/nahlady-s/trnava/12-3-1-1-13.jpg',
    resp = requests.get('http://www.ponuka.nubium.sk/rp/{0}/{1}/{2}.jpg'.format(type, mesto, id),
         auth=HTTPBasicAuth('nubium', 'objednat'))
         #cookies = auth)
    if resp.ok and resp.headers['Content-Type'] == 'image/jpeg':
        with open(DATA_DIR+type+'/'+id+'.jpg', 'wb') as ff:
            ff.write(resp.content)
    else:
        err_writer.writerow([id, mesto, type])

with codecs.open(DATA_FILE, mode='r') as ff:
    csvreader = csv.reader(ff, delimiter=';')
    for row in csvreader:
        if len(row) > 8:
            id = row[1].replace('/','-')
            mesto = unidecode(row[4].decode('cp1250')).lower().replace(' - ', '-').replace(' ','-')
            picture(id, mesto, 'foto')
            picture( id, mesto, 'mapy')
            #print row[1], unidecode(mesto)

ERR_FILE.close()
