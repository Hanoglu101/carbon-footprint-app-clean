from database import session
from models import User
import streamlit_authenticator as stauth

# 🔐 Parola hash'leme
hashed_password = stauth.Hasher(['12345']).generate()[0]

# 👤 Yeni kullanıcı oluştur
new_user = User(
    name="Ayşe Yılmaz",
    email="ayse.yilmaz@hotmail.com",
    password=hashed_password
)

# 💾 Veritabanına ekle
session.add(new_user)
session.commit()

print("✅ Ayşe Yılmaz başarıyla eklendi.")
