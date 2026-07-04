from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kunci_rahasia_proyek_mhs_123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Model Database untuk Admin
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Model Database untuk Data Mahasiswa
class Mahasiswa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nim = db.Column(db.String(20), unique=True, nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    jurusan = db.Column(db.String(100), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Form Validasi menggunakan Flask-WTF
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Daftar')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username sudah digunakan, cari yang lain!')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# --- ROUTING / PATH APLIKASI ---

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Akun berhasil dibuat! Silakan login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Selamat datang kembali!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login gagal. Periksa username dan password Anda!', 'danger')
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    data_mahasiswa = Mahasiswa.query.all()
    return render_template('dashboard.html', mahasiswa=data_mahasiswa)

@app.route('/tambah', methods=['GET', 'POST'])
@login_required
def tambah_mhs():
    if request.method == 'POST':
        nim = request.form.get('nim')
        nama = request.form.get('nama')
        email = request.form.get('email')
        jurusan = request.form.get('jurusan')
        
        # Cek NIM duplikat
        cek_nim = Mahasiswa.query.filter_by(nim=nim).first()
        if cek_nim:
            flash('NIM sudah terdaftar di sistem!', 'danger')
            return redirect(url_for('tambah_mhs'))

        mhs_baru = Mahasiswa(nim=nim, nama=nama, email=email, jurusan=jurusan)
        db.session.add(mhs_baru)
        db.session.commit()
        flash('Data mahasiswa berhasil ditambahkan!', 'success')
        return redirect(url_for('dashboard'))
        
    return render_template('tambah_mhs.html')

@app.route('/hapus/<int:id>')
@login_required
def hapus_mhs(id):
    mhs = Mahasiswa.query.get_or_404(id)
    db.session.delete(mhs)
    db.session.commit()
    flash('Data mahasiswa berhasil dihapus!', 'warning')
    return redirect(url_for('dashboard'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Anda telah keluar dari sistem.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Membuat file database otomatis jika belum ada
    app.run(debug=True)