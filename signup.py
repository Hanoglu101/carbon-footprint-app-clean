import streamlit as st
import bcrypt
from database import session
from models import User

st.set_page_config(page_title="Kayıt Ol", layout="centered")
st.title("📝 Kullanıcı Kayıt Sayfası")

with st.form("signup_form"):
    name = st.text_input("Adınız Soyadınız")
    email = st.text_input("E-posta")
    password = st.text_input("Şifre", type="password")
    submit = st.form_submit_button("Kayıt Ol")

if submit:
    if not name or not email or not password:
        st.warning("Lütfen tüm alanları doldurun.")
    else:
        # E-posta zaten kayıtlı mı kontrol et
        existing_user = session.query(User).filter_by(email=email).first()
        if existing_user:
            st.warning("Bu e-posta ile kayıtlı bir kullanıcı zaten var.")
        else:
            import streamlit_authenticator as stauth
            hashed_password = stauth.Hasher([password]).generate()[0]
            new_user = User(name=name, email=email, password=hashed_password)
            session.add(new_user)
            session.commit()
            st.success("🎉 Kayıt başarılı! Artık giriş yapabilirsiniz.")
