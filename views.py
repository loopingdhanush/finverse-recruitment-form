from flask import Blueprint,render_template,request
import requests
views = Blueprint('views', __name__)

@views.route('/')
def login():
    return render_template('index.html')

@views.route('/home', methods=['POST'])
def home():
    username = request.form['username']
    password = request.form['password']

    api_url="https://psgtech-profile-scrapper.onrender.com/api/userinfo"
    response = requests.post(api_url, json={
        'username': username,
        'password': password
    })

    response_data = response.json()
    name = response_data["Name"]
    roll = response_data["Roll"]
    batch = response_data["Batch"]
    course = response_data["Course"]
    semester = response_data["Semester"]
    email = response_data["Email"]
    contact = response_data["Contact"]

    return render_template('profile.html', name=name, roll=roll, batch=batch, course=course, semester=semester, email=email, contact=contact)
