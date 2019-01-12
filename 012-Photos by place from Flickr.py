from flask import Flask, render_template
from requests import get

app = Flask(__name__)


@app.route('/flickr/photos_by_place/<string:place>')
def photos_by_place(place):
    return render_template('012-Photos by place from Flickr.html', place=place, photo_url_list=photos_from_place(place))

def coords(place):
    return get('http://maps.googleapis.com/maps/api/geocode/json?address='+place+'&sensor=true').json()['results'][0]['geometry']['location']

def photos_from_place(place):
    loc = coords(place)
    photos = get('https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=7b222539666086a11f9d2ed798c05236&lat='+str(loc['lat'])+'&lon='+str(loc['lng'])+'&radius=0.05&per_page=500&format=json&nojsoncallback=1').json()['photos']['photo']
    photo_urls = []
    for photo in photos:
        photo_urls.append(f"http://farm{photo['farm']}.staticflickr.com/{photo['server']}/{photo['id']}_{photo['secret']}.jpg")
    return photo_urls