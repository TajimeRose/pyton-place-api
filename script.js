const axios = require('axios');
const fs = require('fs');

const API_KEY = 'AIzaSyAP3MjfWq561cbV08c6uN1TvsTS9YfkKKY'; // ใส่ API Key ของคุณ
const location = '13.8808,100.5955';
const radius = 50000;
const keyword = encodeURIComponent('ร้านซ่อมรถยนต์');

async function getPlaces() {
    const url = `https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=${location}&radius=${radius}&keyword=${keyword}&key=${API_KEY}`;
    const res = await axios.get(url);
    return res.data.results;
}

async function getPlaceDetails(place_id) {
    const fields = [
        'name',
        'formatted_address',
        'geometry',
        'url',
        'opening_hours',
        'formatted_phone_number',
        'website',
        'photo',
        'rating',
        'review'
    ].join(',');
    const url = `https://maps.googleapis.com/maps/api/place/details/json?place_id=${place_id}&fields=${fields}&key=${API_KEY}`;
    const res = await axios.get(url);
    return res.data.result;
}

(async () => {
    try {
        const results = await getPlaces();
        const places_data = [];

        for (let idx = 0; idx < results.length && idx < 10; idx++) {
            const place = results[idx];
            const details = await getPlaceDetails(place.place_id);

            // ดึง url ของรูปทั้งหมด
            let photo_urls = [];
            if (details.photos) {
                photo_urls = details.photos.map(photo =>
                    `https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=${photo.photo_reference}&key=${API_KEY}`
                );
            }

            // ดึงรีวิว (เฉพาะข้อความ)
            let reviews = [];
            if (details.reviews) {
                reviews = details.reviews.map(r => r.text).filter(Boolean);
            }

            const place_info = {
                name: `${idx + 1}. ${details.name}`,
                address: details.formatted_address,
                rating: details.rating,
                location: details.geometry ? details.geometry.location : null,
                url: details.url,
                opening_hours: details.opening_hours ? details.opening_hours.weekday_text : null,
                phone: details.formatted_phone_number,
                website: details.website,
                photo_urls: photo_urls,
                reviews: reviews
            };

            places_data.push(place_info);
        }

        fs.writeFileSync('Tats.json', JSON.stringify(places_data, null, 4), 'utf8');
        console.log('ดึงข้อมูลสำเร็จ บันทึกลง Tats.json แล้ว');
    } catch (err) {
        console.error(err);
    }
})();