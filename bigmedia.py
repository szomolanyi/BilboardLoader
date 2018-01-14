import os.path
import csv
import codecs
from threading import Thread
import time
import logging
import uploader
import re

# umiestnenie fotiek a map
DATA_DIR= 'C:/work/web/BIlboards-data/bigmedia/all'
# datovy csv subor
DATA_FILE = 'C:/work/web/BIlboards-data/bigmedia/bigmedia-nosice_1250.csv'
#DATA_FILE = 'C:/work/web/BIlboards-data/nubium/Nubium-pokus.csv'
#DATA_FILE = 'C:/work/web/BIlboards-data/nubium/Nubium-ponukat1.csv'
MAX=uploader.THREADS*4


logging.basicConfig(filename='basic.log',level=logging.DEBUG)

def add_desc(desc, item):
    if item is not None and len(item)>0:
        if len(desc) > 0:
            desc += ', ' + item
        else:
            desc = item
    return desc


def run():
    uploader.start()
    current = 0
    with codecs.open(DATA_FILE, mode='r') as ff:
        csvreader = csv.reader(ff, delimiter=';')
        for row in csvreader:
            if len(row) > 8:
                desc = add_desc('', row[4])
                desc = add_desc(desc, row[6])
                desc = add_desc(desc, row[8])
                desc = add_desc(desc, row[9])
                native_id_tmp = row[0]
                files = {
                    'company_id':(None, '5'),
                    'native_id':(None, native_id_tmp),
                    'type':(None,  row[7]),
                    'region':(None,  row[1].decode('cp1250').encode('utf-8')),
                    'district':(None,  row[2].decode('cp1250').encode('utf-8')),
                    'city':(None,  row[3].decode('cp1250').encode('utf-8')),
                    'street':(None,  row[5].decode('cp1250').encode('utf-8')),
                    'description':(None,  desc.decode('cp1250').encode('utf-8')),
                    'lat':(None, row[12].replace(',','.')),
                    'lng':(None, row[13].replace(',','.')),
                }
                #files = dict()
                photo = '{0}/photos/{1}.jpg'.format(DATA_DIR, native_id_tmp[3:])
                mapa = '{0}/maps/{1}m.jpg'.format(DATA_DIR, native_id_tmp[3:])
                if os.path.isfile(photo) == True:
                    files['picture_file'] = open(photo,'rb')
                if os.path.isfile(mapa) == True:
                    files['map_picture_file'] = open(mapa,'rb')
                if current > MAX:
                    item = uploader.not_queue.get()
                    current -= 1
                uploader.data_queue.put(files)
                current += 1
    time.sleep(100)

if __name__ == "__main__":
    run()
