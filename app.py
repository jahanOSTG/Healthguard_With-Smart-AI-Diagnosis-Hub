from flask import Flask, render_template, redirect, url_for, session, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
import bcrypt
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import os

from flask_mysqldb import MySQL

from ml_heart_model import predict_heart
from ml_diabetic_model import predict_diabetes




import MySQLdb.cursors


app = Flask(__name__)

# MySQL Config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Janie900272@'
app.config['MYSQL_DB'] = 'mydatabase'
app.secret_key = 'your_secret_key_here'  # Replace with your own strong key

mysql = MySQL(app)

# ---------------- Register Form ---------------- #
class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_email(self, field):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (field.data,))
        user = cursor.fetchone()
        cursor.close()
        if user:
            raise ValidationError("Email already registered.")

# ---------------- Login Form ---------------- #
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

# ---------------- Home Page ---------------- #
@app.route('/')
def index():
    return render_template('index.html')

# ---------------- Register ---------------- #
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
            mysql.connection.commit()
            cursor.close()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            flash(f"Database Error: {str(e)}", "danger")

    return render_template('register.html', form=form)

# ---------------- Login ---------------- #
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            session['user_id'] = user[0]
            return redirect(url_for('dashboard1'))
        else:
            flash("Invalid email or password.", "danger")
            return redirect(url_for('login'))

    return render_template('login.html', form=form)

# ---------------- Dashboard ---------------- #
@app.route('/dashboard1')
def dashboard1():
    if 'user_id' in session:
        user_id = session['user_id']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            return render_template('dashboard1.html', user=user)

    flash("Please log in first.", "warning")
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please log in first.")
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("You have been logged out successfully.", "success")
    return redirect(url_for('login'))

# ---------------- Contact ---------------- #
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        try:
            cursor = mysql.connection.cursor()
            cursor.execute(
                "INSERT INTO contact_messages (name, email, message) VALUES (%s, %s, %s)",
                (name, email, message)
            )
            mysql.connection.commit()
            cursor.close()
            flash('Message sent successfully!', 'success')
        except Exception as e:
            flash(f'Database Error: {str(e)}', 'danger')
        
        return redirect(url_for('contact'))

    return render_template('contact.html')

@app.route('/diabetes')
def diabetes():
    return render_template('diabetes.html')


@app.route('/predict_diabetes', methods=['POST'])
def predict_diabetes_route():
    # Extract data from form inputs
    data = [
        float(request.form['pregnancies']),
        float(request.form['glucose']),
        float(request.form['bloodpressure']),
        float(request.form['skinthickness']),
        float(request.form['insulin']),
        float(request.form['bmi']),
        float(request.form['dpf']),
        float(request.form['age'])
    ]

    # Use the prediction function from ml_diabetic_model.py
    prediction = predict_diabetes(data)

    # Prepare user-friendly message
    result = "The person is Diabetic" if prediction == 1 else "The person is Not Diabetic"

    return render_template('diabetes.html', prediction_text=result)


@app.route('/show_diabetes_report', methods=['POST'])
def show_diabetes_report():
    input_data = {
        'pregnancies': request.form['pregnancies'],
        'glucose': request.form['glucose'],
        'bloodpressure': request.form['bloodpressure'],
        'skinthickness': request.form['skinthickness'],
        'insulin': request.form['insulin'],
        'bmi': request.form['bmi'],
        'dpf': request.form['dpf'],
        'age': request.form['age'],
        'result': request.form['result']
    }
    return render_template('diabetes_report.html', data=input_data)



# 1️⃣ Route to show heart disease form
@app.route('/heart')
def heart():
    return render_template('heart.html')





# 3️⃣ Route to show heart disease report
@app.route('/predict_heart', methods=['POST'])
def predict_heart_report():
    # Extract form data
    input_data = [
        float(request.form['age']),
        float(request.form['sex']),
        float(request.form['cp']),
        float(request.form['trestbps']),
        float(request.form['chol']),
        float(request.form['fbs']),
        float(request.form['restecg']),
        float(request.form['thalach']),
        float(request.form['exang']),
        float(request.form['oldpeak']),
        float(request.form['slope']),
        float(request.form['ca']),
        float(request.form['thal'])
    ]

    # Make prediction
    prediction = predict_heart(input_data)
    result_text = "The person has Heart Disease" if prediction == 1 else "The person is Healthy"

    # Prepare data for the report template
    report_data = {
        'age': request.form['age'],
        'sex': request.form['sex'],
        'cp': request.form['cp'],
        'trestbps': request.form['trestbps'],
        'chol': request.form['chol'],
        'fbs': request.form['fbs'],
        'restecg': request.form['restecg'],
        'thalach': request.form['thalach'],
        'exang': request.form['exang'],
        'oldpeak': request.form['oldpeak'],
        'slope': request.form['slope'],
        'ca': request.form['ca'],
        'thal': request.form['thal'],
        'result': result_text
    }

    # Render the heart report directly
    return render_template('heart_report.html', data=report_data)






@app.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        date = request.form.get('date')
        time = request.form.get('time')
        doctor = request.form.get('doctor')
        message = request.form.get('message')

        if not (name and email and date and time and doctor):
            flash("Please fill in all required fields.", "danger")
            return redirect(url_for('book_appointment'))

        try:
            cursor = mysql.connection.cursor()
            insert_query = """
                INSERT INTO appointments (name, email, phone, date, time, doctor, message)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (name, email, phone, date, time, doctor, message))
            mysql.connection.commit()
            cursor.close()
            flash("Appointment successfully booked!", "success")
            return redirect(url_for('login'))
        except Exception as e:
            flash(f"Database error: {str(e)}", "danger")
            return redirect(url_for('book_appointment'))

    return render_template('book_appointment.html')


@app.route('/blood_bank', methods=['GET', 'POST'])
def blood_bank():
    if request.method == 'POST':
        donor_name = request.form['donor_name']
        email = request.form['email']
        phone = request.form['phone']
        blood_group = request.form['blood_group']
        last_donation = request.form.get('last_donation')
        health_condition = request.form.get('health_condition')

        # Save this info to your database here

        flash('Thank you for your donation registration!', 'success')
        return redirect(url_for('blood_bank'))

    return render_template('blood_bank.html')

@app.route('/donors', methods=['GET', 'POST'])
def donors():
    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        donor_name = request.form['donor_name']
        email = request.form['email']
        phone = request.form['phone']
        blood_group = request.form['blood_group']
        last_donation = request.form.get('last_donation')
        health_condition = request.form.get('health_condition')

        cursor.execute("""
            INSERT INTO donors (donor_name, email, phone, blood_group, last_donation, health_condition)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (donor_name, email, phone, blood_group, last_donation, health_condition))
        mysql.connection.commit()

        flash('🎉 Congratulations! You have successfully joined as a donor.', 'success')

    cursor.execute("SELECT * FROM donors ORDER BY created_at DESC")
    donor_list = cursor.fetchall()
    cursor.close()

    return render_template('donors.html', donors=donor_list)




@app.route('/blood-groups')
def blood_groups():
    groups = [
        {"name": "A+", "liters": 12},
        {"name": "A-", "liters": 5},
        {"name": "B+", "liters": 8},
        {"name": "B-", "liters": 3},
        {"name": "O+", "liters": 15},
        {"name": "O-", "liters": 2},
        {"name": "AB+", "liters": 6},
        {"name": "AB-", "liters": 1}
    ]
    return render_template("blood_groups.html", groups=groups)


# ---------------- Admin Login ---------------- #
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM admin WHERE email = %s", (email,))
        admin = cursor.fetchone()
        cursor.close()

        # Compare plain password directly
        if admin and password == admin[3]:
            session['admin_id'] = admin[0]
            session['admin_email'] = admin[2]
            flash("Login successful!", "success")
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid email or password. Try again.", "danger")
            return redirect(url_for('admin_login'))

    return render_template('admin_login.html')



@app.route('/add_doctor', methods=['POST'])
def add_doctor():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']  # Make sure your form has phone field
    specialty = request.form['specialty']
    photo = request.files['photo']

    filename = None
    if photo:
        filename = photo.filename
        save_path = os.path.join('static', 'img', filename)  # save in static/img
        os.makedirs(os.path.dirname(save_path), exist_ok=True)  # create folder if not exist
        photo.save(save_path)

    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO doctors (name, email, phone, specialty, image) VALUES (%s, %s, %s, %s, %s)",
        (name, email, phone, specialty, filename)
    )
    mysql.connection.commit()
    cursor.close()
    flash('Doctor added successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        flash("Please log in to access the admin dashboard.", "warning")
        return redirect(url_for('admin_login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Fetch users
    cursor.execute("SELECT id, name, email FROM users")
    users = cursor.fetchall()

    # Fetch appointments
    cursor.execute("SELECT id, name, email, phone, date, time, doctor FROM appointments")
    appointments = cursor.fetchall()

    # Fetch donors
    cursor.execute("SELECT id, donor_name, email, phone, blood_group FROM donors")
    donors = cursor.fetchall()

    # Fetch admins
    cursor.execute("SELECT id, username, email, created_at FROM admin")
    admins = cursor.fetchall()
    
    # Fetch contact messages
    cursor.execute("SELECT id, name, email, message, submitted_at FROM contact_messages")
    contact_messages = cursor.fetchall()
    
    # Fetch doctors
    cursor.execute("SELECT id, name, email, phone, specialty, image FROM doctors")

    doctors = cursor.fetchall()

    cursor.close()

    return render_template('admin_dashboard.html', 
                           users=users, 
                           appointments=appointments, 
                           donors=donors, 
                           admins=admins,
                           contact_messages=contact_messages,
                           doctors=doctors,  # pass doctors to template
                           admin_email=session['admin_email'])
    
    


@app.route('//doctors_page')
def doctors_page():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM doctors")
    doctors = cursor.fetchall()
    cursor.close()
    return render_template('doctors_page.html', doctors=doctors)





# ---------------- Admin Logout ---------------- #
@app.route('/admin/logout')
def admin_logout():
    session.clear()
    flash("You have been logged out!", "info")
    return redirect(url_for('admin_login'))




if __name__ == '__main__':
    app.run(debug=True)





