from flask import Flask, render_template, url_for, redirect
import json

app = Flask(__name__)


@app.route('/')
def index():
    # قراءة بيانات الدول من ملف JSON
    with open('data/countries.json') as f:
        countries = json.load(f)
    
    # قراءة بيانات الأماكن من ملف JSON
    with open('data/places.json') as f:
        places = json.load(f)
    
    # تمرير البيانات إلى القالب
    return render_template('index.html', countries=countries, places=places)

@app.route('/place/<int:place_id>')
def place(place_id):
    # هنا يمكنك جلب بيانات المكان باستخدام place_id
    # مثال:
    with open('data/places.json') as f:
        places = json.load(f)
        place = next((p for p in places if p['id'] == place_id), None)
    return render_template('place.html', place=place)


@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
