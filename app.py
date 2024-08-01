from uuid import uuid4
from flask import Flask, request, jsonify, render_template
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
import json


app = Flask(__name__)
CORS(app)  # تفعيل CORS لجميع المسارات

# تهيئة JWT
app.config['JWT_SECRET_KEY'] = 'your_secret_key'
jwt = JWTManager(app)


# قراءة بيانات المستخدمين والأماكن
users_file_path = 'data/users.json'
places_file_path = 'data/places.json'

with open(users_file_path) as f:
    users = json.load(f)

with open(places_file_path) as f:
    places = json.load(f)

# تخزين المراجعات الجديدة في الذاكرة
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
        # إذا لم يتم العثور على المستخدم، إنشاء مستخدم جديد
        new_user = {
            "id": str(len(users) + 1),
            "email": email,
            "password": password,
            "name": email.split('@')[0]  # استخدام الجزء الأول من البريد الإلكتروني كاسم
        }
        users.append(new_user)
        
        # كتابة المستخدم الجديد إلى ملف JSON
        with open(users_file_path, 'w') as f:
            json.dump(users, f, indent=4)

        user = new_user

    access_token = create_access_token(identity=user['id'])
    return jsonify(access_token=access_token)


@app.route('/')
def index():
    with open('data/countries.json') as f:
        countries = json.load(f)
    with open('data/places.json') as f:
        places = json.load(f)
    return render_template('index.html', countries=countries, places=places)

@app.route('/place/<int:place_id>')
def place(place_id):
    with open('data/places.json') as f:
        places = json.load(f)
        place = next((p for p in places if p['id'] == place_id), None)
    return render_template('place.html', place=place)

if __name__ == '__main__':
    app.run(debug=True)
