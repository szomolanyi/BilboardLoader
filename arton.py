import os.path
import csv
import codecs
from threading import Thread
import time
import logging
import uploader
import re
import requests

# umiestnenie fotiek a map
DATA_DIR= 'C:/work/web/BIlboards-data/arton'
# datovy csv subor
DATA_FILE = 'C:/work/web/BIlboards-data/arton/plochy_1250.csv'
#DATA_FILE = 'C:/work/web/BIlboards-data/nubium/Nubium-pokus.csv'
#DATA_FILE = 'C:/work/web/BIlboards-data/nubium/Nubium-ponukat1.csv'
MAX=uploader.THREADS*4
FORMAT = '%(asctime)-15s %(levelname)s %(module)-8s %(message)s'


logging.basicConfig(filename='basic.log',level=logging.DEBUG, format=FORMAT)

def run():
    uploader.set_cfg('pgdev')
    print uploader.cfg
    s = requests.Session()
    cookies = uploader.login(s)
    with codecs.open(DATA_FILE, mode='r') as ff:
        csvreader = csv.reader(ff, delimiter=';')
        for row in csvreader:
            if len(row) > 8:
                try:
                    native_id_tmp = row[0]
                    files = {
                        'company_id':(None, '6'),
                        'native_id':(None, native_id_tmp),
                        'type':(None,  ''),
                        'region':(None,  row[3].decode('cp1250').encode('utf-8')),
                        'district':(None,  row[1].decode('cp1250').encode('utf-8')),
                        'city':(None,  row[4].decode('cp1250').encode('utf-8')),
                        'street':(None,  row[5].decode('cp1250').encode('utf-8')),
                        'description':(None,  row[6].decode('cp1250').encode('utf-8')),
                        'lat':(None, row[9]),
                        'lng':(None, row[10]),
                    }
                    #files = dict()
                    '''
                    photo = '{0}/{1}'.format(DATA_DIR, row[51])
                    mapa = '{0}/{1}'.format(DATA_DIR, row[52])
                    if os.path.isfile(photo) == True:
                        files['picture_file'] = open(photo,'rb')
                    if os.path.isfile(mapa) == True:
                        files['map_picture_file'] = open(mapa,'rb')
                    '''
                    uploader.upload(s, cookies, files)
                except Exception as e:
                    logging.exception('Chyba')
                    s.close()
                    time.sleep(3)
                    logging.info('======= Restarting sesssion')
                    s = requests.Session()
                    cookies = uploader.login(s)
    time.sleep(100)

if __name__ == "__main__":
    run()
