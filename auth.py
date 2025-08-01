from sqlalchemy.orm import Session
from models import User
import bcrypt

# Şifreyi hashleyen fonksiyon
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Şifreyi kontrol eden fonksiyon
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Kullanıcı kaydını veritabanına ekleme
def register_user(db: Session, username: str, full_name: str, email: str, password: str) -> bool:
    existing_user = db.query(User).filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return False  # kullanıcı varsa kayıt olamaz

    hashed_pw = hash_password(password)
    new_user = User(username=username, full_name=full_name, email=email, password_hash=hashed_pw)
    db.add(new_user)
    db.commit()
    return True

# Giriş yapmaya çalışan kullanıcıyı doğrulama
def login_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if user and verify_password(password, user.password_hash):
        return user
    return None
