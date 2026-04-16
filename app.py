from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from email_validator import validate_email, EmailNotValidError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registrations.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

db = SQLAlchemy(app)

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(100), nullable=False)
    team_leader = db.Column(db.String(100), nullable=False)
    members = db.Column(db.Text, nullable=False)  # comma separated
    emails = db.Column(db.Text, nullable=False)  # comma separated
    utr = db.Column(db.String(50), unique=True, nullable=False)
    screenshot_path = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    team_name = request.form['team_name']
    team_leader = request.form['team_leader']
    members = request.form['members']
    emails = request.form['emails']
    utr = request.form['utr']
    file = request.files['screenshot']

    # Validate emails
    email_list = [e.strip() for e in emails.split(',')]
    for email in email_list:
        try:
            validate_email(email)
        except EmailNotValidError:
            flash(f'Invalid email: {email}')
            return redirect(url_for('index'))

    # Check UTR unique
    if Registration.query.filter_by(utr=utr).first():
        flash('UTR number already exists. Please use a unique UTR.')
        return redirect(url_for('index'))

    # Save file
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
    else:
        flash('Invalid file type. Only PNG, JPG, JPEG allowed.')
        return redirect(url_for('index'))

    # Save to db
    reg = Registration(team_name=team_name, team_leader=team_leader, members=members, emails=emails, utr=utr, screenshot_path=filename)
    db.session.add(reg)
    db.session.commit()

    flash('Registration and payment submission successful!')
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    if 'admin' not in session:
        return redirect(url_for('login'))
    regs = Registration.query.all()
    return render_template('admin.html', regs=regs)

@app.route('/admin/team/<int:id>')
def team_detail(id):
    if 'admin' not in session:
        return redirect(url_for('login'))
    reg = Registration.query.get_or_404(id)
    return render_template('team_detail.html', reg=reg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            session['admin'] = True
            return redirect(url_for('admin'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)