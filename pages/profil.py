import streamlit as st
from database import session
from models import User
import bcrypt

st.set_page_config(page_title="Profil", layout="centered")

# Kullanıcı oturumunu kontrol et
if 'username' not in st.session_state:
    st.warning("Lütfen önce giriş yapın.")
    st.stop()

# Giriş yapan kullanıcının bilgilerini al
user_email = st.session_state['username']
user = session.query(User).filter_by(email=user_email).first()

st.title("👤 Profil Bilgileri")
st.markdown(f"*Ad Soyad:* {user.name}")
st.markdown(f"*E-posta:* {user.email}")

st.divider()

# 🔁 Ad Soyad Güncelleme
with st.expander("📝 Ad Soyad Güncelle"):
    new_name = st.text_input("Yeni Ad Soyad", value=user.name)
    if st.button("Ad Soyadı Güncelle"):
        user.name = new_name
        session.commit()
        st.success("✅ Ad Soyad başarıyla güncellendi.")
        st.experimental_rerun()

# 🔐 Şifre Güncelleme
with st.expander("🔒 Şifreyi Güncelle"):
    current_password = st.text_input("Mevcut Şifre", type="password")
    new_password = st.text_input("Yeni Şifre", type="password")
    confirm_password = st.text_input("Yeni Şifre (Tekrar)", type="password")

    if st.button("Şifreyi Güncelle"):
        if not bcrypt.checkpw(current_password.encode(), user.password.encode()):
            st.error("❌ Mevcut şifre hatalı.")
        elif new_password != confirm_password:
            st.error("❌ Yeni şifreler eşleşmiyor.")
        else:
            hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
            user.password = hashed_password
            session.commit()
            st.success("✅ Şifre başarıyla güncellendi.")
