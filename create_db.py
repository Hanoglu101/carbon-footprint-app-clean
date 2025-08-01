from models import Base, engine, EmissionFactor
from database import session

# Tabloları oluştur
Base.metadata.create_all(engine)
print("✅ Veritabanı başarıyla oluşturuldu: karbon_app.db")

# Örnek veri (sadece bir kere çalıştır)
sample_factors = [
    EmissionFactor(category="Elektrik", unit="kWh", emission_factor=0.233, source="IEA", region="TR"),
    EmissionFactor(category="Doğalgaz", unit="m³", emission_factor=2.02, source="EPA", region="TR"),
    EmissionFactor(category="Benzin", unit="litre", emission_factor=2.31, source="DEFRA", region="TR"),
    EmissionFactor(category="Dizel", unit="litre", emission_factor=2.68, source="DEFRA", region="TR"),
    EmissionFactor(category="Uçuş", unit="km", emission_factor=0.09, source="ICAO", region="TR")
]

session.add_all(sample_factors)
session.commit()
print("✅ Örnek emisyon faktörleri eklendi.")

