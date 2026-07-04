from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Inisialisasi awal database
db = SQLAlchemy()

# Class Model untuk Admin (Authentication)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    # Method OOP untuk hashing password biar aman
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Method OOP untuk ngecek kecocokan password pas login
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Class Model untuk Data Mahasiswa (Operasi CRUD)
class Mahasiswa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nim = db.Column(db.String(15), unique=True, nullable=False) # Mencegah duplikasi NIM
    nama = db.Column(db.String(100), nullable=False)
    jurusan = db.Column(db.String(100), nullable=False)
    ipk = db.Column(db.Float, nullable=False)