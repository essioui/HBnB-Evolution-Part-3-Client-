from flask import Flask, render_template, url_for, redirect
import json

app = Flask(__name__)

def load_places():
    with open('places.json', 'r') as f:
        return json.load(f)


@app.route('/')
def index():
    with open('places.json', 'r') as f:
        places = json.load(f)

        return render_template('index.html', places=places[:3])

@app.route('/place/<int:place_id>')
def place(place_id):
    places = load_places()
    place = next((p for p in places if p['id'] == place_id), None)
    if place is None:
        return redirect(url_for('index'))
    
    logged_in = True 
    return render_template('place.html', place=place, user_logged_in=logged_in)


@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
