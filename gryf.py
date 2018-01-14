
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
DATA_DIR= 'C:/work/web/BIlboards-data/gryf'
# datovy csv subor
DATA_FILE = 'C:/work/web/BIlboards-data/gryf/MDS-databaza.dbf'
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
    for row in DBF(DATA_FILE, encoding='cp852'):
        try:
            desc = add_desc('', row['USEK_SMER'])
            desc = add_desc(desc, row['OSADENIE'])
            native_id_tmp = str(row['CISLO'])
            (lat, lng) = row['GPS'].split(',')
            files = {
                'company_id':(None, '4'),
                'native_id':(None, native_id_tmp),
                'type':(None,  row['TYP'].encode('utf-8')),
                'region':(None,  ''),
                'district':(None,  ''),
                'city':(None,  row['LOKALITA'].encode('utf-8')),
                'street':(None,  row['ULICA_CEST'].encode('utf-8')),
                'description':(None,  desc.encode('utf-8')),
                'lat':(None, lat.strip()),
                'lng':(None, lng.strip()),
            }
            #files = dict()
            photo = '{0}{1}'.format(DATA_DIR, row['OBRAZOK'])
            mapa = '{0}{1}'.format(DATA_DIR, row['MAPA'])
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
