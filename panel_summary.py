from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Project, ActivityData
import pandas as pd

# Veritabanı bağlantısı
engine = create_engine('sqlite:///karbon_app.db')
Session = sessionmaker(bind=engine)
session = Session()

# Kullanıcı e-postası
user_email = "ayse@example.com"

# Kullanıcıyı sorgula
user = session.query(User).filter_by(email=user_email).first()

if user:
    total_projects = session.query(Project).filter_by(user_id=user.id).count()
    total_activities = session.query(ActivityData).filter_by(user_id=user.id).count()
    total_emission = session.query(ActivityData).filter_by(user_id=user.id).with_entities(
        ActivityData.total_emission).all()
    total_emission_sum = sum([em[0] for em in total_emission if em[0] is not None])

    summary_data = {
        "Kullanıcı Adı": user.name,
        "Toplam Proje Sayısı": total_projects,
        "Toplam Faaliyet Sayısı": total_activities,
        "Toplam Emisyon (kg CO₂e)": round(total_emission_sum, 2)
    }

    df = pd.DataFrame([summary_data])
    print(df.to_markdown(index=False))
else:
    print("❌ Kullanıcı bulunamadı.")
