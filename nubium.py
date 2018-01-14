import os.path
import csv
import codecs
from threading import Thread
import time
import logging
import uploader

# umiestnenie fotiek a map
DATA_DIR= 'C:/work/web/BIlboards-data/nubium/'
# datovy csv subor
DATA_FILE = 'C:/work/web/BIlboards-data/nubium/Nubium-ponuka-1765525-vsetky.csv'
#DATA_FILE = 'C:/work/web/BIlboards-data/nubium/Nubium-pokus.csv'
#DATA_FILE = 'C:/work/web/BIlboards-data/nubium/Nubium-ponukat1.csv'
MAX=uploader.THREADS*4
FORMAT = '%(asctime)-15s %(levelname)s %(module)-8s %(message)s'

logging.basicConfig(filename='basic.log',level=logging.DEBUG, format=FORMAT)

def run():
    uploader.start()
    current = 0
    with codecs.open(DATA_FILE, mode='r') as ff:
        csvreader = csv.reader(ff, delimiter=';')
        for row in csvreader:
            if len(row) > 8:
                native_id_tmp = row[1]
                files = {
                    'company_id':(None, '1'),
                    'native_id':(None, native_id_tmp),
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
