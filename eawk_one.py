
import os.path
import csv
import codecs
from threading import Thread
import time
import logging
import uploader
import re
import requests
from dbfread import DBF


# umiestnenie fotiek a map
DATA_DIR= 'C:/work/web/BIlboards-data/eawk/all'
# datovy csv subor
DATA_FILE = 'C:/work/web/BIlboards-data/eawk/DATA/nosic.dbf'
#DATA_FILE = 'C:/work/web/BIlboards-data/nubium/Nubium-pokus.csv'
#DATA_FILE = 'C:/work/web/BIlboards-data/nubium/Nubium-ponukat1.csv'
MAX=uploader.THREADS*4
FORMAT = '%(asctime)-15s %(levelname)s %(module)-8s %(message)s'


logging.basicConfig(filename='basic.log',level=logging.DEBUG, format=FORMAT)

def add_desc(desc, item):
    if item is not None and len(item)>0:
        if len(desc) > 0:
            desc += ', ' + item
        else:
            desc = item
    return desc



def run():
    uploader.set_cfg('prod')
    print uploader.cfg
    s = requests.Session()
    cookies = uploader.login(s)
    for row in DBF(DATA_FILE):
        try:
            desc = add_desc('', row['CTVRT'])
            desc = add_desc(desc, row['UL_CIS1'])
            native_id_tmp = str(row['E_CIS'])
            files = {
                'company_id':(None, '3'),
                'native_id':(None, native_id_tmp),
                'type':(None,  row['VELIKOST'].encode('utf-8')),
                'region':(None,  row['KRAJ'].encode('utf-8')),
                'district':(None,  row['OKRES'].encode('utf-8')),
                'city':(None,  row['MESTO'].encode('utf-8')),
                'street':(None,  row['UL_CIS'].encode('utf-8')),
                'description':(None,  desc.encode('utf-8')),
                'lat':(None, str(row['VGS84_N'])),
                'lng':(None, str(row['VGS84_EO'])),
            }
            #files = dict()
            photo = '{0}/photos/{1}.jpg'.format(DATA_DIR, native_id_tmp[2:])
            mapa = '{0}/maps/{1}m.jpg'.format(DATA_DIR, native_id_tmp[2:])
            if os.path.isfile(photo) == True:
                files['picture_file'] = open(photo,'rb')
            if os.path.isfile(mapa) == True:
                files['map_picture_file'] = open(mapa,'rb')
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
