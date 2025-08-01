from models import EmissionFactor, Session

session = Session()

sample_data = [
    {"category": "Elektrik", "material": "Şebeke Elektriği", "unit": "kWh", "emission_factor": 0.233, "source": "Ecoinvent", "region": "TR"},
    {"category": "Elektrik", "material": "Yenilenebilir Enerji", "unit": "kWh", "emission_factor": 0.0, "source": "Ecoinvent", "region": "TR"},
    {"category": "Ulaşım", "material": "Dizel Araç", "unit": "litre", "emission_factor": 2.68, "source": "DEFRA", "region": "TR"},
    {"category": "Ulaşım", "material": "Benzinli Araç", "unit": "litre", "emission_factor": 2.31, "source": "DEFRA", "region": "TR"},
    {"category": "Isıtma", "material": "Doğalgaz", "unit": "m3", "emission_factor": 1.9, "source": "EPA", "region": "TR"},
    {"category": "Isıtma", "material": "Kömür", "unit": "kg", "emission_factor": 2.5, "source": "EPA", "region": "TR"},
    {"category": "Atık", "material": "Organik Atık", "unit": "kg", "emission_factor": 0.5, "source": "IPCC", "region": "TR"},
    {"category": "Atık", "material": "Plastik Atık", "unit": "kg", "emission_factor": 1.2, "source": "IPCC", "region": "TR"},
]

for data in sample_data:
    emission_factor = EmissionFactor(**data)
    session.add(emission_factor)

session.commit()
print("✅ Örnek emisyon faktörleri başarıyla eklendi!")
