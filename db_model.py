"""
@DATE: 2022/5/3
@Author  : ld
"""
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from conf import SQLITE_DB


engine = create_engine(url=SQLITE_DB, echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)()

class BaseArea(object):

    name = Column(String(256))
    parent_code = Column(Integer, default=0)  # 父级行政区域编码
    ad_code = Column(Integer, default=0)  # 行政区域编码
    card_code = Column(Integer, default=0)  # 身份证ID编码
    phone_code = Column(String(32), default=0)  # 长途区号
    mail_code = Column(Integer, default=0)  # 邮政编码
    car_code = Column(String(32), default=0)  # 车牌编码
    center_area = Column(String(256))  # 行政驻地


    @classmethod
    def commit(self):
        Session.commit()

    @classmethod
    def add_all(cls, list):
        Session.add_all(list)
        cls.commit()

    def add_and_flush(self):
        Session.add(self)
        Session.flush()
        return self

    def add_and_commit(self):
        Session.add(self)
        Session.commit()
        return self

    def get(self, id, to_dict=False):
        res = Session.query(self).get(id)
        return res.to_dict() if res and to_dict else res

    def get_by(self, to_dict=False, **kwargs):
        res = Session.query(self).filter_by(**kwargs).all()
        if not res:
            return []
        return [i.to_dict() for i in res] if to_dict else res


class Province(Base, BaseArea):

    __tablename__ = "province"

    province_id = Column(Integer, primary_key=True, autoincrement=True)
    level = Column(String(256), default="省")  # 行政区域级别


class City(Base, BaseArea):

    __tablename__ = "city"

    city_id = Column(Integer, primary_key=True, autoincrement=True)
    province_id = Column(Integer, nullable=True)
    level = Column(String(256), default="市")  # 行政区域级别


class County(Base, BaseArea):

    __tablename__ = "county"

    county_id = Column(Integer, primary_key=True, autoincrement=True)
    city_id = Column(Integer, nullable=True)
    level = Column(String(256), default="地级市")  # 行政区域级别


class Town(Base, BaseArea):

    __tablename__ = "town"

    town_id = Column(Integer, primary_key=True, autoincrement=True)
    county_id = Column(Integer, nullable=True)
    level = Column(String(256), default="镇/乡")  # 行政区域级别


class Village(Base, BaseArea):

    __tablename__ = "village"

    village_id = Column(Integer, primary_key=True, autoincrement=True)
    town_id = Column(Integer, nullable=True)
    level = Column(String(256), default="村")  # 行政区域级别


Base.metadata.create_all(bind=engine, checkfirst=True)
