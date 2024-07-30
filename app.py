from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/place')
def place():
    place = {
        'name': 'Beautiful Beach House',
        'host': 'John Doe',
        'price_per_night': 100,
        'location': 'Los Angeles, United States',
        'description': 'A beautiful beach house with amazing views.',
        'amenities': 'WiFi, Pool, Air Conditioning'
    }
    user_logged_in = True 
    return render_template('place.html', place=place, user_logged_in=user_logged_in)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
