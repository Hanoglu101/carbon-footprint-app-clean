from sqlalchemy.orm import declarative_base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///karbon_app.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
