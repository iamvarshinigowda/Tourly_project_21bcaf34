from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os
app = Flask(__name__)

# PostgreSQL database configuration
DB_HOST = 'host.docker.internal'
DB_NAME = 'Tourly'
DB_USER = 'postgres'
DB_PASSWORD = 'Man_2507'
DB_PORT='5433'

# Connect to PostgreSQL database
def connect_db():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        return conn
    except psycopg2.Error as e:
        print("Unable to connect to the database:", e)
        return None

# Error handling for database connection
@app.errorhandler(psycopg2.Error)
def handle_database_error(error):
    return render_template('error.html', message="Database Error: Unable to connect to the database. Please try again later."), 500

# Route for index page (dashboard)
@app.route('/')
def index():
    # Render the index page
    return render_template('index.html')

# Route for registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Insert data into database
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO registration (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
                conn.commit()
                cur.close()
                conn.close()
                # Redirect to login page after registration
                return redirect(url_for('login'))
            except psycopg2.Error as e:
                print("Error inserting data into the database:", e)
                conn.rollback()
                cur.close()
                conn.close()
                # Render registration form with error message
                return render_template('registrationform.html', error="An error occurred during registration. Please try again.")
        else:
            # Render registration form with error message
            return render_template('registrationform.html', error="Unable to connect to the database. Please try again later.")

    # Render registration form
    return render_template('registrationform.html')

# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']

        # Check if username and password exist in database
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM registration WHERE username = %s AND password = %s", (username, password))
            user = cur.fetchone()
            cur.close()
            conn.close()

            if user:
                # User found, redirect to dashboard
                return redirect(url_for('index'))
            else:
                # User not found, render login page with error message
                return render_template('login.html', error="Invalid username or password. Please try again.")
        else:
            # Render login page with error message
            return render_template('login.html', error="Unable to connect to the database. Please try again later.")

    # Render login form
    return render_template('login.html')

# Route for booking form

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        # Get form data
        destination = request.form['destination']
        numpeople = request.form['numpeople']
        checkindate = request.form['checkindate']
        checkoutdate = request.form['checkoutdate']
        price = request.form['price']

        # Insert data into database
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO booking (destination, numpeople, checkindate, checkoutdate, price) VALUES (%s, %s, %s, %s, %s)", 
                            (destination, numpeople, checkindate, checkoutdate, price))
                conn.commit()
                cur.close()
                conn.close()
                # Redirect to success page after insertion
                return redirect(url_for('payment'))
            except psycopg2.Error as e:
                print("Error inserting data into the database:", e)
                conn.rollback()
                cur.close()
                conn.close()
                # Render booking form with error message
                return render_template('book.html', error="An error occurred during booking. Please try again.")
        else:
            # Render booking form with error message
            return render_template('book.html', error="Unable to connect to the database. Please try again later.")
    return render_template('book.html')

        
# Route for contact us form
@app.route('/contactus', methods=['GET', 'POST'])
def contactus():
    if request.method == 'POST':
        # Get form data
        Name = request.form['Name']
        Contactnumber = request.form['Contact_number']
        Message = request.form['Message']

        # Insert contact us data into database
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO contactus (Name, Contact_number, Message) VALUES (%s, %s, %s)", 
                            (Name, Contactnumber, Message))
                conn.commit()
                cur.close()
                conn.close()
                # Redirect to index page after contact us submission
                return redirect(url_for('index'))
            except psycopg2.Error as e:
                print("Error inserting contact us data into the database:", e)
                conn.rollback()
                cur.close()
                conn.close()
                # Render contact us form with error message
                return render_template('contactus.html', error="An error occurred during contact us submission. Please try again.")
        else:
            # Render contact us form with error message
            return render_template('contactus.html', error="Unable to connect to the database. Please try again later.")
    
    # Render contact us form
    return render_template('contactus.html')


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        try:
            namefeedback = request.form['name']
            rating = request.form['rating']
            suggestion = request.form['suggestion']

            conn = connect_db()
            if conn:
                cur = conn.cursor()
                try:
                    cur.execute("INSERT INTO feedback (namefeedback, rating, suggestion) VALUES (%s, %s, %s)",
                                (namefeedback, rating, suggestion))
                    conn.commit()
                    cur.close()
                    conn.close()
                    return "Thank you, " + namefeedback + ", for your valuable feedback! You rated us: " + rating
                except psycopg2.Error as e:
                    print("Error inserting data into the database:", e)
                    conn.rollback()
                    cur.close()
                    conn.close()
                    return "An error occurred while submitting feedback. Please try again."
            else:
                return "Unable to connect to the database. Please try again later."
        except KeyError:
            return "Form data is missing required fields."
    elif request.method == 'GET':
        return render_template('demo.html')  # Render the feedback form template
    else:
        return "Method not allowed. Please use GET or POST method."

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        card_number = request.form.get('cardNumber')
        card_holder = request.form.get('cardHolder')
        expiry_date = request.form.get('expiryDate')
        cvv = request.form.get('cvv')

        # Insert card payment information into the payment table
        conn = connect_db()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO payment (card_number, card_holder, expiry_date, cvv) VALUES (%s, %s, %s, %s)",
                            (card_number, card_holder, expiry_date, cvv))
                conn.commit()
                cur.close()
                conn.close()
                # Redirect to success page after insertion
                return redirect(url_for('index'))
            except psycopg2.Error as e:
                print("Error inserting payment data into the database:", e)
                conn.rollback()
                cur.close()
                conn.close()
                # Render payment form with error message
                return render_template('payment.html', error="An error occurred during payment. Please try again.")
        else:
            # Render payment form with error message
            return render_template('payment.html', error="Unable to connect to the database. Please try again later.")

    # Render the payment form
    return render_template('payment.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)








