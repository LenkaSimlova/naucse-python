from datetime import datetime
import os, sys
import shutil
from collections import defaultdict
from exif import Image
import html_script

def get_coord(coord, direct):
    if coord is None or direct is None:
        return None
    d, m, s = coord
    d += m/60 + s/3600
    if direct in ('S', 'W'):
        d *= -1
    return d

def zpracuj_exif (cesta, fotka):
    with open(os.path.join(cesta, fotka), 'rb') as image_file:
        my_image = Image(image_file)
    #datum
    date = my_image.get('datetime')
    if date is not None:
        date = datetime.strptime(date, '%Y:%m:%d %H:%M:%S')
        year = str(date.year)
        output_date = date.strftime('%Y-%m-%d')
    else:
        year = 'Unknown'
        output_date = 'Unknown'
    #GPS data
    longitude = my_image.get('gps_longitude')
    longitude_ref = my_image.get('gps_longitude_ref')
    latitude = my_image.get('gps_latitude')
    latitude_ref = my_image.get('gps_latitude_ref')
    exif_fotky = {
        'datetime': date,
        'longitude': get_coord(longitude, longitude_ref),
        'latitude': get_coord(latitude, latitude_ref),
        'old_name': fotka,
        'new_name': None,
        'year': year,
        'output_date': output_date,
        'new_path': None,
    }
    return exif_fotky

#získání vstupu
if len(sys.argv) < 3:
    print('špatný vstup')
    sys.exit()
input_dir = sys.argv[1]
output_dir = sys.argv[2]
mazani = '-x' in sys.argv[3:]
mapa = '-m' in sys.argv[3:]

#čte exif data a třídí je podle data pořízení
photos_by_date = defaultdict(list)
for photo in os.listdir(input_dir):
    if photo.lower().endswith('.jpeg') or photo.lower().endswith('.jpg'):
        photo_exif = zpracuj_exif(input_dir, photo)
        output_date = photo_exif['output_date']
        photos_by_date[output_date].append(photo_exif)

#vytvoření výstupní adresář, pokud neexistuje
os.makedirs(output_dir, exist_ok=True)

#oindexování fotek
for datum, seznam_fotek in photos_by_date.items():
    for index, fotka in enumerate(seznam_fotek, start=1):
        fotka['new_name'] = f"{datum}-{index}.jpg"
        fotka['new_path'] = os.path.join(fotka['year'], fotka['new_name'])
        os.makedirs(
            os.path.join(output_dir, fotka['year']),
            exist_ok=True
            )
        old_path = os.path.join(input_dir, fotka['old_name'])
        new_path = os.path.join(output_dir, fotka['year'], fotka['new_name'])
        try:
            shutil.copy2(old_path, new_path)
        except shutil.Error:
            print(new_path+' již existuje!')

#mazání fotek
if mazani:
    odpoved_mazani = input('Chcete fotku smazat? [a/N]').lower()
    while odpoved_mazani not in ('a', 'n', ''):
        odpoved_mazani = input('Chcete fotku smazat? Zadejte pouze [a/N]!').lower()
    if odpoved_mazani == 'a':
        for seznam_fotek in photos_by_date.values():
            for fotka in seznam_fotek:
                old_path = os.path.join(input_dir, fotka['old_name'])
                os.remove(old_path)
                print('Byla smazána fotka:', old_path)

#mapa
fotky_s_GPS = []

for seznam_fotek in photos_by_date.values():
    for fotka in seznam_fotek:
        if fotka['longitude'] is not None and fotka['latitude'] is not None:
            fotky_s_GPS.append(fotka)
            del fotka['datetime']

with open(os.path.join(output_dir, 'mapa.html'), 'w') as soubor_s_mapou:
    soubor_s_mapou.write(html_script.zacatek)
    soubor_s_mapou.write(str(fotky_s_GPS)+';')
    soubor_s_mapou.write(html_script.konec)
