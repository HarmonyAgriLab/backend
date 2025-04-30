from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
from fastapi.responses import FileResponse

from get_config import *

from publish import publish_ceiling, publish_fan, publish_curtain, publish_heater

mysql_config_list = get_mysql_config()
username = mysql_config_list['username']
password = mysql_config_list['password']
host = mysql_config_list['host']
port = mysql_config_list['port']
database = mysql_config_list['database']

# 数据库连接配置
DATABASE_URL = "mysql+mysqlconnector://" + username + ":" + password + "@" + host + ":" + str(port) + "/" + database

# 创建数据库引擎
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
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

# FastAPI 应用
app = FastAPI()

# 依赖项：获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 查询 air 表的最新 20 条数据
@app.get("/air", response_model=List[AirResponse])
def get_air_data(db: Session = Depends(get_db)):
    air_data = db.query(Air).order_by(Air.id.desc()).limit(20).all()
    return air_data

# 查询 soil 表的最新 20 条数据
@app.get("/soil", response_model=List[SoilResponse])
def get_soil_data(db: Session = Depends(get_db)):
    soil_data = db.query(Soil).order_by(Soil.id.desc()).limit(20).all()
    return soil_data

# 获取图片
@app.get("/images/{image_name}")
async def get_image(image_name: str):
    image_path = f'/root/images/{image_name}'
    return FileResponse(image_path, media_type = 'image/png')

# 控制棚顶开合
@app.get("/controll/ceiling/{status}")
def controll_ceiling(status: str):
    try:
        status_int = int(status)
        publish_ceiling(status_int)
        result = {
            "code": 0,
            "message": "Success." 
        }
        return result
    except ValueError:
        result = {
            "code": 1,
            "message": "Fail, invalid type of status."
        }
        return result
    except Exception as e:
        result = {
            "code": 1,
            "message": "Fail, unexpected error occurred."
        }

# 控制排风扇开关
@app.get("/controll/fan/{status}")
def controll_fan(status: str):
    try:
        status_int = int(status)
        publish_fan(status_int)
        result = {
            "code": 0,
            "message": "Success."
        }
        return result
    except ValueError:
        result = {
            "code": 1,
            "message": "Fail, invalid type of status."
        }
        return result
    except Exception as e:
        result = {
            "code": 1,
            "message": "Fail, unexpected error occurred."
        }

# 控制遮阳帘开闭
@app.get("/controll/curtain/{status}")
def controll_curtain(status: str):
    try:
        status_int = int(status)
        publish_curtain(status_int)
        result = {
            "code": 0,
            "message": "Success."
        }
        return result
    except ValueError:
        result = {
            "code": 1,
            "message": "Fail, invalid type of status."
        }
        return result
    except Exception as e:
        result = {
            "code": 1,
            "message": "Fail, unexpected error occurred."
        }

# 控制地暖开关
@app.get("/controll/heater/{status}")
def controll_heater(status: str):
    try:
        status_int = int(status)
        publish_heater(status_int)
        result = {
            "code": 0,
            "message": "Success."
        }
        return result
    except ValueError:
        result = {
            "code": 1,
            "message": "Fail, invalid type of status."
        }
        return result
    except Exception as e:
        result = {
            "code": 1,
            "message": "Fail, unexpected error occurred."
        }

# 启动应用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
