from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from backend.database.connection import Base

class ChargingOrder(Base):
    __tablename__ = "charging_order"
    
    id = Column(Integer, primary_key=True, index=True)
    order_no = Column(String(50), unique=True, index=True)
    user_id = Column(Integer, index=True)
    station_id = Column(Integer, index=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    charging_amount = Column(Float)
    power_consumed = Column(Float)
    unit_price = Column(Float)
    total_cost = Column(Float)
    status = Column(String(20))

class ChargingStation(Base):
    __tablename__ = "charging_station"
    
    id = Column(Integer, primary_key=True, index=True)
    station_name = Column(String(100), index=True)
    address = Column(String(200))
    city = Column(String(50))
    province = Column(String(50))
    total_piles = Column(Integer)
    available_piles = Column(Integer)
    operator = Column(String(100))
    status = Column(String(20))

class UserRecord(Base):
    __tablename__ = "user_record"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True)
    username = Column(String(50), unique=True)
    phone = Column(String(20))
    register_time = Column(DateTime)
    total_charging_count = Column(Integer)
    total_charging_amount = Column(Float)
    total_power_consumed = Column(Float)
    is_active = Column(Boolean, default=True)
