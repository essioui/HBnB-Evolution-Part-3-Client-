from flask import Flask, request, jsonify, render_template
from flask_jwt_extended import JWTManager, create_access_token
from flask_cors import CORS
import json, os

app = Flask(__name__)
CORS(app)

# JWT
app.config['JWT_SECRET_KEY'] = 'your_secret_key'
jwt = JWTManager(app)

# Read data
users_file_path = 'data/users.json'
places_file_path = 'data/places.json'

with open(users_file_path) as f:
    users = json.load(f)

with open(places_file_path) as f:
    places = json.load(f)

with open('data/countries.json', 'r') as f:
    countries = json.load(f)

# Store in new memory
new_reviews = []

@app.route('/login', methods=['GET'])
def show_login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    user = next((u for u in users if u['email'] == email and u['password'] == password), None)

    if not user:
        return jsonify({"msg": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user['id'])
    return jsonify(access_token=access_token)

@app.route('/')
def index():
    with open('data/countries.json') as f:
        countries = json.load(f)
    with open('data/places.json') as f:
        places = json.load(f)
    return render_template('index.html', countries=countries, places=places)

@app.route('/places')
def places():
    country_name = request.args.get('country', default='', type=str)
    
    # قراءة بيانات الأماكن من ملف JSON
    with open('data/places.json', 'r') as file:
        places = json.load(file)
    
    # تصفية الأماكن حسب البلد إذا تم تحديد بلد معين
    if country_name:
        places = [place for place in places if place['country_name'] == country_name]
    
    return render_template('places.html', places=places, selected_country=country_name)

@app.route('/place/<int:place_id>')
def place(place_id):
    file_path = os.path.join('data', 'places.json')
    with open(file_path, 'r') as file:
        places = json.load(file)

    place = next((p for p in places if p['id'] == place_id), None)

    if place:
        return render_template('place.html', place=place)
    else:
        return "Place not found", 404

if __name__ == '__main__':
    app.run(debug=True, port=8000)
