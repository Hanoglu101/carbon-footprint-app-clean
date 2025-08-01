from sqlalchemy import create_engine, Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    projects = relationship("Project", back_populates="user")
    activities = relationship("ActivityData", back_populates="user")

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    total_emission_kg = Column(Float)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="projects")

    activities = relationship("ActivityData", back_populates="project")

class ActivityData(Base):
    __tablename__ = 'activity_data'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    category = Column(String)
    subcategory = Column(String)
    activity = Column(String)
    unit = Column(String)
    amount = Column(Float)
    emission_factor = Column(Float)
    total_emission = Column(Float)
    region = Column(String)
    source = Column(String)
    scope = Column(String)

    project = relationship("Project", back_populates="activities")
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="activities")

class EmissionFactor(Base):
    __tablename__ = "emission_factors"

    id = Column(Integer, primary_key=True)
    category = Column(String)
    material = Column(String)
    unit = Column(String)
    emission_factor = Column(Float)
    source = Column(String)
    region = Column(String)

# Veritabanı motoru
engine = create_engine('sqlite:///karbon_app.db')
Session = sessionmaker(bind=engine)
