from sqlalchemy import Column, Integer, String, Float, DateTime
try:
    from database import Base
except ImportError:
    from backend.database import Base
import datetime

class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    lot_id = Column(String, unique=True, index=True)
    supplier_name = Column(String)
    supplier_phone = Column(String)
    state = Column(String, default="Maharashtra")
    variety = Column(String, default="nashik_red")
    grade = Column(String, default="Grade A")
    size_class = Column(String, default="Medium")
    moisture = Column(Float, default=12.0)
    sprouting = Column(Float, default=0.0)
    damage = Column(Float, default=0.0)
    doubles = Column(Float, default=0.0)
    inspector_name = Column(String, default="")
    notes = Column(String, default="")
    computed_score = Column(Integer, default=100)
    quality_status = Column(String, default="CERTIFIED")
    images = Column(String, default="")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class OnionVariety(Base):
    __tablename__ = "onion_varieties"
    code = Column(String, primary_key=True)
    name = Column(String)
    variety_type = Column(String, default="Rabi / Storage")
    origin = Column(String)
    characteristics = Column(String, default="")
    image_url = Column(String, default="")
    order = Column(Integer, default=0)

class DefectSample(Base):
    __tablename__ = "defect_samples"
    sample_id = Column(String, primary_key=True)
    title = Column(String)
    tag = Column(String)
    class_tag = Column(String)
    tag_bg = Column(String, default="")
    badge_bg = Column(String, default="")
    image_url = Column(String, default="")
    description = Column(String, default="")
    order = Column(Integer, default=0)
