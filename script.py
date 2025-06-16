import googlemaps
import json
from datetime import datetime


API_KEY = ''
gmaps = googlemaps.Client(key=API_KEY)

# กำหนดพิกัด และ keyword ที่ต้องการค้นหา
location = (13.8808, 100.5955)  
radius = 50000 # 50 กิโลเมตร
keyword = 'ร้านซ่อมรถยนต์'


results = gmaps.places_nearby(location=location, radius=radius, keyword=keyword)

places_data = []


for idx, place in enumerate(results.get('results', [])):
    if idx >= 1:  
        break
    place_id = place['place_id']


    details = gmaps.place(place_id=place_id, fields=[
        'name',
        'formatted_address',
        'geometry',
        'url',
        'opening_hours',
        'formatted_phone_number',
        'website',
        'photo',
        'rating',   # เพิ่ม field rating
        'review'    # เพิ่ม field review
    ])
    result = details.get('result', {})
    # ดึง url ของรูปทั้งหมด (ถ้ามี)
    photo_urls = []
    photos = result.get('photos')
    if photos:
        for photo in photos:
            photo_reference = photo.get('photo_reference')
            if photo_reference:
                url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={API_KEY}"
                photo_urls.append(url)

    # ดึงรีวิว (เฉพาะข้อความ)
    reviews = []
    for review in result.get('reviews', []):
        text = review.get('text')
        if text:
            reviews.append(text)

    place_info = {
        'name': f"{idx+1}. {result.get('name')}",
        'address': result.get('formatted_address'),
        'rating': result.get('rating'),
        'location': result.get('geometry', {}).get('location'),
        'url': result.get('url'),
        'opening_hours': result.get('opening_hours', {}).get('weekday_text'),
        'phone': result.get('formatted_phone_number'),
        'website': result.get('website'),
        'photo_urls': photo_urls,
        'reviews': reviews                  
    }



    places_data.append(place_info)


with open('Tats.json', 'w', encoding='utf-8') as f:
    json.dump(places_data, f, ensure_ascii=False, indent=4)

print(" ดึงข้อมูลสำเร็จ บันทึกลง Tats.json แล้ว")
