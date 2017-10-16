import requests
from requests.auth import HTTPBasicAuth
import csv
import codecs
from unidecode import unidecode

import nubium_main

DATA_FILE = 'C:/work/web/BilboardLoader/errtmp.csv'
ERR_FILE = open('err2.csv', 'wb')
err_writer = csv.writer(ERR_FILE, delimiter=';')

mesto_repar= {
    'bratislava-ruzinov':'ba-ruzinov',
    'bratislava-podunajske-biskupice':'ba-pod-biskupice',
    'bratislava-stare-mesto':'ba-stare-mesto',
    'ziar-nad-hronom-ladomerska-vieska':'ziar-nad-hronom',
    'bratislava-vrakuna':'ba-vrakuna',
    'bratislava-nove-mesto':'ba-nove-mesto',
    'bratislava-raca':'ba-raca',
    'bratislava-vajnory':'ba-vajnory',
    'bratislava-devinska-nova-ves':'ba-dnv',
    'bratislava-dubravka':'ba-dubravka',
    'bratislava-karlova-ves':'ba-karlova-ves',
    'bratislava-zahorska-bystrica':'ba-zahorska-bystrica',
    'bratislava-lamac':'ba-lamac',
    'bratislava-devin':'ba-devin',
    'bratislava-petrzalka':'ba-petrzalka',
    'bratislava-cunovo':'ba-cunovo',
    'bratislava-jarovce':'ba-jarovce',
    'bratislava-rusovce':'ba-rusovce',
    'stupava-mast':'stupava',
    'kosice-sever':'ke-sever',
    'kosice-sidlisko-tahanovce':'ke-sidl-tahanovce',
    'kosice-stare-mesto':'ke-stare-mesto',
    'kosice-dzungla':'ke-dzungla',
    'kosice-saca':'ke-saca',
    'kosice-zapad':'ke-zapad',
    'kosice-polov':'ke-polov',
    'kosice-myslava':'ke-myslava',
    'kosice-lunik-ix.':'ke-lunik-ix',
    'kosice-sidlisko-kvp':'ke-sidlisko-kvp',
    'kosice-peres':'ke-peres',
    'kosice-vysne-opatske':'ke-vysne-opatske',
    'kosice-dargovskych-hrdinov':'ke-darg-hrdinov',
    'kosice-kosicka-nova-ves':'ke-knv',
    'kosice-juh':'ke-juh',
    'kosice-krasna':'ke-krasna',
    'kosice-nad-jazerom':'ke-nad-jazerom',
    'kosice-barca':'ke-barca',
    'kosice-sebastovce':'ke-sebastovce',
    'ivanka-pri-nitre':'ivanka-pre-nitre',
    'surany-cast-albertov-dvor':'albertov-dvor',
    'presov-haniska':'presov',
    'presov-lubotice':'presov',
    'dubnica-nad-vahom':'dubnica',
    'plevnik-drienove':'plevnik',
    'zabokreky-nad-nitrou':'zabokreky',
    'nitra-juzny-obchvat':'nitra',
    'liptovska-osada':'lip.osada',
    'liptovsky-mikulas-demanova':'demanova',
    'galanta-kosuty':'galanta',
}

with codecs.open(DATA_FILE, mode='r') as ff:
    csvreader = csv.reader(ff, delimiter=';')
    for row in csvreader:
        id = row[0]
        typ = row[2]
        mesto = row[1]
        if (mesto in mesto_repar.keys()):
            ret = nubium_main.picture(id, mesto_repar[mesto], typ)
            if ret == False:
                err_writer.writerow([id, mesto, typ])

ERR_FILE.close()
