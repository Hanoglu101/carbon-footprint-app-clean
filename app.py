import streamlit as st
import streamlit_authenticator as stauth
from database import session
from models import Project, ActivityData, EmissionFactor, User
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import io
import openai
import os
from dotenv import load_dotenv

st.set_page_config(page_title="Karbon Ayak İzi Uygulaması", layout="centered")

# 🌍 API Anahtarını yükle
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 🔐 Dinamik kullanıcı yapılandırması
users = session.query(User).all()
user_credentials = {}

for user in users:
    user_credentials[user.email] = {
        'name': user.name,
        'password': user.password  # hashed şifre!
    }

config = {
    'credentials': {
        'usernames': user_credentials
    },
    'cookie': {
        'name': 'karbonai_cookie',
        'key': 'random_signature_key',
        'expiry_days': 30
    },
    'preauthorized': {
        'emails': [u.email for u in users]
    }
}

# 🧠 Giriş sistemini başlat
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# 🧾 Giriş ekranı
name, authentication_status, username = authenticator.login('main')

if authentication_status:
    st.session_state["username"] = username  # Bu önemli!
    st.sidebar.success(f"Hoş geldin, {name} 👋")
    authenticator.logout('Çıkış Yap', 'sidebar')

    st.title("🌱 Karbon Ayak İzi Hesaplama Uygulaması")

    # Giriş yapan kullanıcıyı al
    logged_in_user = session.query(User).filter_by(email=username).first()

    # ➕ Proje Oluşturma
    st.header("📦 Proje Oluştur")
    with st.form("project_form"):
        name_input = st.text_input("Proje Adı")
        location = st.text_input("Konum")
        start_date = st.date_input("Başlangıç Tarihi")
        end_date = st.date_input("Bitiş Tarihi")
        submitted = st.form_submit_button("Proje Ekle")

    if submitted:
        new_project = Project(
            name=name_input,
            location=location,
            start_date=start_date,
            end_date=end_date,
            user=logged_in_user
        )
        session.add(new_project)
        session.commit()
        st.success("✅ Proje başarıyla eklendi!")

    # 🔽 Proje Seçimi
    st.header("📘 Faaliyet Girişi")
    project_list = session.query(Project.name).filter_by(user_id=logged_in_user.id).all()
    project_names = [p[0] for p in project_list]

    if project_names:
        selected_project_name = st.selectbox("Proje Seç", project_names)
        selected_project = session.query(Project).filter_by(name=selected_project_name, user_id=logged_in_user.id).first()
        st.info(f"Seçilen proje: {selected_project.name}")

        # Faaliyet Ekleme
        with st.form("activity_form"):
            category_options = session.query(EmissionFactor.category).distinct().all()
            category_options = [c[0] for c in category_options]
            category = st.selectbox("Faaliyet Kategorisi", category_options)
            source = st.text_input("Kaynak Açıklaması")
            amount = st.number_input("Miktar", min_value=0.0, step=0.1)
            scope = st.selectbox("Emisyon Kapsamı (Scope)", ["Scope 1", "Scope 2", "Scope 3"])

            factor = session.query(EmissionFactor).filter_by(category=category).first()
            unit = factor.unit if factor else "-"
            emission_factor = factor.emission_factor if factor else 0.0

            st.write(f"📐 Birim: {unit}")
            st.write(f"🌍 Emisyon Katsayısı: {emission_factor} kg CO₂e/{unit}")

            submit_activity = st.form_submit_button("Faaliyet Ekle")

        if submit_activity:
            emission = amount * emission_factor
            new_activity = ActivityData(
                project_id=selected_project.id,
                category=category,
                source=source,
                amount=amount,
                unit=unit,
                emission_factor=emission_factor,
                total_emission=emission,
                scope=scope,
                user_id=logged_in_user.id
            )
            session.add(new_activity)
            if selected_project.total_emission_kg is None:
                selected_project.total_emission_kg = 0.0
            selected_project.total_emission_kg += emission
            session.commit()
            st.success(f"✅ Faaliyet başarıyla eklendi! Toplam emisyon: {emission:.2f} kg CO₂e")

            # Öneri Sistemi
            with st.expander("💡 Yapay Zekâdan Öneri Al"):
                prompt = f"""
                Aşağıdaki faaliyet için sürdürülebilirlik önerileri üret:
                - Kategori: {category}
                - Kaynak: {source}
                - Miktar: {amount} {unit}
                - Emisyon: {emission:.2f} kg CO₂e
                Lütfen karbon ayak izini azaltmaya yönelik 2 pratik öneri ver.
                """
                try:
                    response = openai.chat.completions.create(
                        model="gpt-4",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    suggestion = response.choices[0].message.content
                    st.write(suggestion)
                except Exception as e:
                    st.error(f"Öneri alınamadı: {str(e)}")

        # 📊 Grafik Gösterimi
        st.header("📈 Emisyon Analizi")
        activities = session.query(ActivityData).filter_by(project_id=selected_project.id).all()
        if activities:
            categories = [a.category for a in activities]
            emissions = [a.total_emission for a in activities]

            fig, ax = plt.subplots()
            ax.bar(categories, emissions)
            ax.set_xlabel("Kategori")
            ax.set_ylabel("Toplam Emisyon (kg CO₂e)")
            ax.set_title("Kategoriye Göre Emisyonlar")
            st.pyplot(fig)

            st.subheader("📘 Scope Bazlı Emisyon Dağılımı")
            scopes = ["Scope 1", "Scope 2", "Scope 3"]
            scope_emissions = [sum(a.total_emission for a in activities if a.scope == scope) for scope in scopes]

            fig2, ax2 = plt.subplots()
            ax2.bar(scopes, scope_emissions)
            ax2.set_xlabel("Emisyon Kapsamı (Scope)")
            ax2.set_ylabel("Toplam Emisyon (kg CO₂e)")
            ax2.set_title("Scope 1-2-3 Emisyon Dağılımı")
            st.pyplot(fig2)

            # ⬇️ Excel çıktısı
            st.subheader("⬇️ Excel Olarak İndir")
            df = pd.DataFrame([{
                "Kategori": a.category,
                "Kaynak": a.source,
                "Miktar": a.amount,
                "Birim": a.unit,
                "Katsayı": a.emission_factor,
                "Toplam Emisyon": a.total_emission,
                "Scope": a.scope
            } for a in activities])

            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Emisyon Verisi')
            st.download_button(
                label="📥 Excel İndir",
                data=buffer.getvalue(),
                file_name="emisyon_verisi.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.info("Henüz faaliyet eklenmedi.")
    else:
        st.warning("Henüz eklenmiş bir proje yok.")
elif authentication_status is False:
    st.error("❌ Kullanıcı adı veya şifre hatalı.")
elif authentication_status is None:
    st.warning("ℹ️ Lütfen giriş yapın.")
