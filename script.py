import googlemaps
import json
from datetime import datetime


API_KEY = 'AIzaSyAP3MjfWq561cbV08c6uN1TvsTS9YfkKKY'
gmaps = googlemaps.Client(key=API_KEY)

# กำหนดพิกัด และ keyword ที่ต้องการค้นหา
location = (13.8808, 100.5955)  
radius = 10000
keyword = 'ร้านซ่อมรถยนต์'


results = gmaps.places_nearby(location=location, radius=radius, keyword=keyword)

places_data = []


for idx, place in enumerate(results.get('results', [])):
    if idx >= 10:
        break
    place_id = place['place_id']

    #  เรียก Place Details API เพื่อดึงข้อมูลเต็ม
    details = gmaps.place(place_id=place_id, fields=[
    'name',
    'formatted_address',
    'geometry',
    'url',
    'opening_hours',
    'rating',
    'user_ratings_total'
])


    result = details.get('result', {})
    place_info = {
        'name': result.get('name'),
        'address': result.get('formatted_address'),
        'location': result.get('geometry', {}).get('location'),
        'url': result.get('url'),
        'opening_hours': result.get('opening_hours', {}).get('weekday_text')
    }

    places_data.append(place_info)


with open('places.json', 'w', encoding='utf-8') as f:
    json.dump(places_data, f, ensure_ascii=False, indent=4)

print(" ดึงข้อมูลสำเร็จ บันทึกลง places.json แล้ว")
