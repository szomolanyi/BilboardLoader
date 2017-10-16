import requests
import os.path
import csv
import codecs

# umiestnenie fotiek a map
DATA_DIR= 'C:/work/web/BIlboards-data/nubium/'
# datovy csv subor
#DATA_FILE = 'C:/work/web/BIlboards-data/nubium/Nubium-ponuka-1765525-vsetky.csv'
DATA_FILE = 'C:/work/web/BIlboards-data/nubium/Nubium-pokus.csv'
# error file
ERR_FILE = open('upl_err.csv', 'wb')
err_writer = csv.writer(ERR_FILE, delimiter=';')


URL='http://localhost:4001/{0}'

def login():
    auth = {
        'email': 'admin',
        'password': 'admin123'
    }
    r = requests.post(URL.format('api/login'), data=auth)
    print r.text
    print r.cookies
    return r.cookies

def get_bilboard(auth):
    r = requests.get(URL.format('api/bilboard/11'), cookies=auth)
    print r.text

def upload(auth, data, files):
    resp = requests.post(URL.format('api/bilboards'), cookies=auth, files=files)
    print resp.text
    return resp.ok

cookies = login()
with codecs.open(DATA_FILE, mode='r') as ff:
    csvreader = csv.reader(ff, delimiter=';')
    for row in csvreader:
        if len(row) > 8:
            native_id_tmp = row[1]
            files = {
                'company_id':(None, '1'),
                'native_id':(None, native_id_tmp+'11'),
                'type':(None,  row[0]),
                'region':(None,  row[2].decode('cp1250').encode('utf-8')),
                'district':(None,  row[3].decode('cp1250').encode('utf-8')),
                'city':(None,  row[4].decode('cp1250').encode('utf-8')),
                'street':(None,  row[5].decode('cp1250').encode('utf-8')),
                'description':(None,  row[6].decode('cp1250').encode('utf-8')),
                'lat':(None, row[7]),
                'lng':(None, row[8]),
            }
            #files = dict()
            photo = '{0}foto/{1}.jpg'.format(DATA_DIR, native_id_tmp.replace('/','-'))
            mapa = '{0}mapy/{1}.jpg'.format(DATA_DIR, native_id_tmp.replace('/','-'))
            if os.path.isfile(photo) == True:
                files['picture_url'] = open(photo,'rb')
            if os.path.isfile(mapa) == True:
                files['map_picture_url'] = open(mapa,'rb')
            res = upload(cookies, None, files)
            if res == False:
                err_writer.writerow([native_id_tmp, None, None])

ERR_FILE.close()
