from flask import Blueprint,render_template,request
import requests
views = Blueprint('views', __name__)
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv() 

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

@views.route('/submit', methods=['POST'])
def submit():
    response_data = request.form

    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    dbname = os.getenv("DB_NAME")

    try:
        connection = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            dbname=dbname
        )
        cursor = connection.cursor()

        # Get form data
        roll = response_data['roll']
        name = response_data['name']
        semester = response_data['semester']
        course = response_data['course']
        batch = response_data['batch']
        email = response_data['email']
        contact = response_data['contact']
        vertical1 = response_data['verticals1']
        reason1 = response_data['reason']
        vertical2 = response_data.get('verticals2', '')  # Optional
        reason2 = response_data.get('reason2', '')        # Optional

        insert_query = """
        INSERT INTO Finverse(
            rollnumber, name, semester, course, batch,
            email, contact, vertical1, vertical1reason,
            vertical2, vertical2reason
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

        data = (
            roll, name, semester, course, batch,
            email, contact, vertical1, reason1, vertical2, reason2
        )

        cursor.execute(insert_query, data)
        connection.commit()

        cursor.close()
        connection.close()
        print("Data inserted and connection closed.")
        return render_template('index2.html')

    except Exception as e:
        print(f"Failed to connect or insert data: {e}")
        return render_template('error.html', error=str(e))