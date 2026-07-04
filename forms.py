from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from models import User, Mahasiswa

# 1. Form untuk Registrasi Akun Admin
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Konfirmasi Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Daftar Admin')

    # Validasi OOP: Mencegah duplikasi username
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username sudah digunakan oleh admin lain.')

    # Validasi OOP: Mencegah duplikasi email
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email sudah terdaftar.')

# 2. Form untuk Login Admin
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# 3. Form untuk Input Data Mahasiswa (CRUD)
class MahasiswaForm(FlaskForm):
    nim = StringField('NIM', validators=[DataRequired(), Length(min=5, max=15)])
    nama = StringField('Nama Lengkap', validators=[DataRequired()])
    jurusan = StringField('Jurusan', validators=[DataRequired()])
    ipk = FloatField('IPK', validators=[DataRequired()])
    submit = SubmitField('Simpan Data')

    def __init__(self, original_nim=None, *args, **kwargs):
        super(MahasiswaForm, self).__init__(*args, **kwargs)
        self.original_nim = original_nim

    # Validasi OOP: Mencegah duplikasi NIM di database
    def validate_nim(self, nim):
        if nim.data != self.original_nim:
            mhs = Mahasiswa.query.filter_by(nim=nim.data).first()
            if mhs:
                raise ValidationError('NIM ini sudah terdaftar di dalam sistem!')