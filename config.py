import os

class Config:
    # Secret key untuk mengamankan form dari serangan luar
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kunci_rahasia_kamu_123'
    
    # Menentukan database menggunakan MySQL XAMPP (Sudah diperbaiki)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/proyek_mhs'
    
    # Mematikan tracking overhead untuk menghemat memori laptop
    SQLALCHEMY_TRACK_MODIFICATIONS = False