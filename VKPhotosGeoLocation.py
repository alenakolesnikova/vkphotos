import vk

import time

print('VK Photos geo location')

session = vk.Session("TOKEN")

api = vk.API(session)

friends = api.friends.get()

friends_info = api.users.get(user_ids=friends)

geolocation = []

# for friend in friends_info:
#    print('ID %s Имя %s %s' % (friend['uid'], friend['last_name'], friend['first_name']))

ph = 0

for id in friends:
    try:
        print('Получаем данные пользователя: %s' % id)
        albums = api.photos.getAlbums(owner_id=id)
        print('\t...альбомов %s...' % len(albums))
        for album in albums:
            photos = api.photos.get(owner_id=id, album_id=album['aid'])
            print('\t\t...обработываем фотографии альбома...')
            for photo in photos:
                # print(photo)
                if 'lat' in photo and 'long' in photo:
                    geolocation.append((photo['lat'], photo['long']))
                    ph += 1
                    # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            print('\t\t...найдено %s фото...' % len(photos))
            time.sleep(0.5)
    except:
        pass
time.sleep(0.5)
print('\n\t\tНайдено %s фото с локацией' % ph)

js_code = ""

iter = 0

for loc in geolocation:
    # print('%s %s' %(loc[0], loc[1]))
    # js_code += 'new google.maps.Marker( position: (lat: %s, lng: %s), map: map);\n' % (loc[0], loc[1])
    loct = 'new google.maps.LatLng(%s, %s)' % (loc[0], loc[1])
    iter += 1
    js_code += 'marker%s = new google.maps.Marker({\n\tmap: map,\n\tposition: %s,\n\tvisible: true\n\t});\n\n' % (iter, loct)

html = open('map.html').read()

html = html.replace('/* PLACEHOLDER */', js_code)

f = open('VKPhotosGeoLocationMap.html', 'w')

f.write(html)

f.close()