import streamlit_authenticator as stauth

# Kullanıcıların şifresi (düz metin halinde)
passwords = ['123', 'admin123']

# Hashlenmiş şifreler
hashed_passwords = stauth.Hasher(passwords).generate()
print(hashed_passwords)
