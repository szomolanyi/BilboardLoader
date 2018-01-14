import requests
import logging
import Queue
from threading import Thread
import json
import csv
import time

THREADS = 1


all_cfg = {
    'test': {
        'URL': 'https://shrouded-atoll-81501.herokuapp.com/{0}',
        'auth': {
            'email': 'admin',
            'password': 'Z@h0rsk@bystr1c@'
        }
    },
    'prod': {
        'URL': 'https://mdservices.herokuapp.com/{0}',
        'auth': {
            'email': 'admin',
            'password': 'Z@h0rsk@bystr1c@'
        }
    },
    'pgdev': {
        'URL': 'http://localhost:4001/{0}',
        'auth': {
            'email': 'admin',
            'password': 'admin123'
        }
    }
}

#cfg = all_cfg['prod']
cfg = all_cfg['prod']

error_queue = Queue.Queue()
data_queue = Queue.Queue()
not_queue = Queue.Queue()

logger = logging.getLogger('uploader')

def set_cfg(type):
    global cfg
    cfg = all_cfg[type]

def login(s=None):
    if s is None:
        logger.info('requests login')
        r = requests.post(cfg['URL'].format('api/login'), data=cfg['auth'])
    else:
        logger.info('session login')
        r = s.post(cfg['URL'].format('api/login'), data=cfg['auth'])
    return r.cookies

def uploader(auth):
    s = requests.Session()
    logger.debug('Uploader start')
    while True:
        try:
            files = data_queue.get(True, 10)
            native_id = files['native_id'][1]
            company_id = files['company_id'][1]
            try:
                upload(s, auth, files)
            except Exception as e:
                logger.exception('Board native_id={0} company_id={1}'.format(native_id, company_id))
                logger.info('Close session')
                time.sleep(15)
                s.close()
                s = requests.Session()
            not_queue.put(0)
        except Queue.Empty:
            pass

def upload(s, auth, files):
    native_id = files['native_id'][1]
    company_id = files['company_id'][1]
    logger.debug('Before get')
    get_path = 'api/bilboards?native_id={0}&company_id={1}'.format(native_id, company_id)
    res = s.get(cfg['URL'].format(get_path), cookies=auth)
    resjs = json.loads(res.text)
    if res.status_code == 200 and len(resjs['data']['rows']) > 0:
        logger.info('Board native_id={0} company_id={1} already uploaded'.format(native_id, company_id))
    else:
        logger.debug('Before post')
        res = s.post(cfg['URL'].format('api/bilboards'), cookies=auth, files=files)
        content = res.content
        text = res.text
        logger.info('Board native_id={0} company_id={1} status={2} {3}'.format(native_id, company_id, res.status_code, content[:10]))
        if 'picture_file' in files:
            files['picture_file'].close()
        if 'map_picture_file' in files:
            files['map_picture_file'].close()
        if res.ok == False:
            logger.error('Board native_id={0} company_id={1} status={2} {3}'.format(native_id, company_id, res.status_code, content))
            error_queue.put((files['native_id'][1], res))
            logger.info('Close session')
            time.sleep(15)
            s.close()
            s = requests.Session()


def get_bilboard(auth, id):
    path = 'api/bilboard/{0}'.format(id)
    r = requests.get(cfg['URL'].format(path), cookies=auth)
    print r.text

def err_writer():
    while True:
        try:
            (native_id_tmp, res) = error_queue.get(True, 10)
            err_data = json.loads(res.text)
            with open('upl_err.csv', 'ab') as ERR_FILE:
                err_writer = csv.writer(ERR_FILE, delimiter=';')
                err_writer.writerow([native_id_tmp, res.status_code, err_data['message'].encode('cp1250')])
        except Queue.Empty:
            pass

def start():
    error_thread = Thread(target=err_writer)
    error_thread.daemon = True
    error_thread.start()
    cookies = login()
    for i in range(0,THREADS):
        up_thread = Thread(target=uploader, args=(cookies,))
        up_thread.daemon = True
        up_thread.start()
