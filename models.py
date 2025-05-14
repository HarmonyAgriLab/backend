from sqlalchemy import Column, Integer, Float, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field
from datetime import datetime

Base = declarative_base()

# 定义 Air 数据模型
class Air(Base):
    __tablename__ = "air"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    air_temp = Column(Float(5, 2), nullable=True)
    air_humid = Column(Float(5, 2), nullable=True)
    device_mac = Column(String(20), nullable=True)
    upload_time = Column(DateTime, nullable=True)

# 定义 Soil 数据模型
class Soil(Base):
    __tablename__ = "soil"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    moisture_value = Column(Float(6, 2), nullable=True)
    temperature_value = Column(Float(6, 2), nullable=True)
    conductivity_value = Column(Float(6, 2), nullable=True)
    pH_value = Column(Float(6, 2), nullable=True)
    nitrogen = Column(Float(6, 2), nullable=True)
    phosphorus = Column(Float(6, 2), nullable=True)
    potassium = Column(Float(6, 2), nullable=True)
    device_mac = Column(String(20), nullable=True)
    upload_time = Column(DateTime, nullable=True)

# Pydantic 模型用于数据验证和序列化
class AirResponse(BaseModel):
    id: int
    air_temp: float | None
    air_humid: float | None
    device_mac: str | None
    upload_time: datetime | None = Field(None, alias="upload_time")

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S") if v else None
        }

class SoilResponse(BaseModel):
    id: int
    moisture_value: float | None
    temperature_value: float | None
    conductivity_value: float | None
    pH_value: float | None
    nitrogen: float | None
    phosphorus: float | None
    potassium: float | None
    device_mac: str | None
    upload_time: datetime | None = Field(None, alias="upload_time")

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S") if v else None
        }