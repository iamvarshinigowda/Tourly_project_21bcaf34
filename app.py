from flask import Flask, render_template, request, redirect, url_for, jsonify
import psycopg2

app = Flask(__name__)

# Database connection settings
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'varshini'
DB_USER = 'varshini'
DB_PASSWORD = 'Man_4569'

def get_user(username):
    try:
        conn = psycopg2.connect(
            host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
        )
        cur = conn.cursor()
        cur.execute("SELECT * FROM registration WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        return user
    except Exception as e:
        return None

@app.route('/')
def index():
    return render_template('registrationform.html')

@app.route('/submit-registration', methods=['POST'])
def submit_registration():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        try:
            # Connect to the PostgreSQL database
            conn = psycopg2.connect(
                host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
            )
            cur = conn.cursor()

            # Insert data into the database
            cur.execute(
                "INSERT INTO registration (username, email, password) VALUES (%s, %s, %s)",
                (username, email, password)
            )
            conn.commit()

            # Close connection
            cur.close()
            conn.close()

            return "Registration details submitted successfully!"
        except Exception as e:
            return "Error: " + str(e)

    return redirect(url_for('index'))

@app.route('/login', methods=['GET'])
def get_user_data(username):
    user = get_user(username)
    if user:
        return jsonify({'username': user[0], 'email': user[1], 'password': user[2]})
    else:
        return jsonify({'error': 'User not found'})

if __name__ == '__main__':
    app.run(debug=True)
