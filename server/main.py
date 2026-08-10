from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from pydantic import BaseModel
from datetime import datetime
import os

app = FastAPI(
    title="ServerSentinel API",
    description="API for ingesting and retrieving server health metrics",
    version="1.0.0"
)

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./metrics.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Model
class SystemMetric(Base):
    __tablename__ = "metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    server_id = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    cpu_percent = Column(Float)
    memory_percent = Column(Float)
    disk_percent = Column(Float)
    bytes_sent = Column(Float)
    bytes_recv = Column(Float)

Base.metadata.create_all(bind=engine)

# Pydantic Model for Input Validation
class MetricCreate(BaseModel):
    server_id: str
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    bytes_sent: float
    bytes_recv: float

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/metrics/", status_code=201)
def create_metric(metric: MetricCreate, db: Session = Depends(get_db)):
    db_metric = SystemMetric(
        server_id=metric.server_id,
        timestamp=datetime.utcnow(),
        cpu_percent=metric.cpu_percent,
        memory_percent=metric.memory_percent,
        disk_percent=metric.disk_percent,
        bytes_sent=metric.bytes_sent,
        bytes_recv=metric.bytes_recv
    )
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return {"status": "success", "id": db_metric.id}

@app.get("/metrics/{server_id}")
def read_metrics(server_id: str, limit: int = 100, db: Session = Depends(get_db)):
    metrics = db.query(SystemMetric).filter(SystemMetric.server_id == server_id)\
                .order_by(SystemMetric.timestamp.desc()).limit(limit).all()
    if not metrics:
        raise HTTPException(status_code=404, detail="Server not found")
    return metrics

@app.get("/servers/")
def list_servers(db: Session = Depends(get_db)):
    servers = db.query(SystemMetric.server_id).distinct().all()
    return [s[0] for s in servers]
