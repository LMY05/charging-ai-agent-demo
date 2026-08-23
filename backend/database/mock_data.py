from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from backend.database.schema import ChargingOrder, ChargingStation, UserRecord
import random

def generate_stations(db: Session):
    stations = [
        {"station_name": "中关村充电站", "address": "北京市海淀区中关村大街1号", "city": "北京", "province": "北京", "total_piles": 12, "available_piles": 8, "operator": "国网充电", "status": "正常运营"},
        {"station_name": "望京SOHO充电站", "address": "北京市朝阳区望京街10号", "city": "北京", "province": "北京", "total_piles": 8, "available_piles": 3, "operator": "特来电", "status": "正常运营"},
        {"station_name": "上海陆家嘴充电站", "address": "上海市浦东新区陆家嘴环路1000号", "city": "上海", "province": "上海", "total_piles": 15, "available_piles": 10, "operator": "星星充电", "status": "正常运营"},
        {"station_name": "深圳科技园充电站", "address": "深圳市南山区科技园南区", "city": "深圳", "province": "广东", "total_piles": 20, "available_piles": 15, "operator": "云快充", "status": "正常运营"},
        {"station_name": "杭州西湖充电站", "address": "杭州市西湖区湖滨银泰附近", "city": "杭州", "province": "浙江", "total_piles": 6, "available_piles": 4, "operator": "国网充电", "status": "维护中"},
    ]
    for s in stations:
        if not db.query(ChargingStation).filter(ChargingStation.station_name == s["station_name"]).first():
            db.add(ChargingStation(**s))
    db.commit()

def generate_users(db: Session):
    users = [
        {"user_id": 1001, "username": "张三", "phone": "13800138001", "register_time": datetime(2024, 1, 15), "total_charging_count": 25, "total_charging_amount": 850.0, "total_power_consumed": 425.0},
        {"user_id": 1002, "username": "李四", "phone": "13800138002", "register_time": datetime(2024, 3, 20), "total_charging_count": 18, "total_charging_amount": 520.0, "total_power_consumed": 260.0},
        {"user_id": 1003, "username": "王五", "phone": "13800138003", "register_time": datetime(2024, 6, 10), "total_charging_count": 12, "total_charging_amount": 380.0, "total_power_consumed": 190.0},
        {"user_id": 1004, "username": "赵六", "phone": "13800138004", "register_time": datetime(2024, 9, 5), "total_charging_count": 8, "total_charging_amount": 260.0, "total_power_consumed": 130.0},
        {"user_id": 1005, "username": "钱七", "phone": "13800138005", "register_time": datetime(2025, 1, 20), "total_charging_count": 5, "total_charging_amount": 150.0, "total_power_consumed": 75.0},
    ]
    for u in users:
        if not db.query(UserRecord).filter(UserRecord.user_id == u["user_id"]).first():
            db.add(UserRecord(**u))
    db.commit()

def generate_orders(db: Session):
    if db.query(ChargingOrder.id).first():
        return

    stations = db.query(ChargingStation).all()
    users = db.query(UserRecord).all()
    
    statuses = ["已完成", "进行中", "已取消"]
    
    for i in range(50):
        station = random.choice(stations)
        user = random.choice(users)
        start_time = datetime.now() - timedelta(days=random.randint(1, 90), hours=random.randint(0, 23))
        duration = random.randint(30, 300)
        end_time = start_time + timedelta(minutes=duration)
        power_consumed = random.uniform(5, 50)
        unit_price = random.uniform(1.0, 1.8)
        total_cost = round(power_consumed * unit_price, 2)
        
        order = ChargingOrder(
            order_no=f"ORD{start_time.strftime('%Y%m%d')}{str(i).zfill(4)}",
            user_id=user.user_id,
            station_id=station.id,
            start_time=start_time,
            end_time=end_time,
            charging_amount=total_cost,
            power_consumed=power_consumed,
            unit_price=unit_price,
            total_cost=total_cost,
            status=random.choice(statuses)
        )
        db.add(order)
    db.commit()

def init_db():
    from backend.database.connection import engine, SessionLocal
    from backend.database.schema import Base
    
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        generate_stations(db)
        generate_users(db)
        generate_orders(db)
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
