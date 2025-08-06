from flask import Flask, render_template, redirect, url_for, session, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
import bcrypt
from flask_mysqldb import MySQL
from ml_diabetic_model import predict_diabetes

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




if __name__ == '__main__':
    app.run(debug=True)
