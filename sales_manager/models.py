from sqlalchemy import event, Column, Integer, String, Float, Date, ForeignKey
from datetime import datetime
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class SalesTable(Base):
    __tablename__ = 'sales_table'
    id = Column(Integer, primary_key=True)
    customer_name = Column(String(50))
    sale_item_name = Column(String(100))
    sale_item_value = Column(Float)
    sale_date = Column(Date, default=datetime.today())

    seller = Column(Integer, ForeignKey("seller.id"))
    sales = relationship("Seller", back_populates="sales")


class Seller(Base):
    __tablename__ = 'seller'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    sales = relationship("SalesTable", back_populates="sales")


def insert_data(target, connection, **kw):
    preloaded_sellers = {
        {'name': 'Cloud Strife'},
        {'name': 'Lara Croft'},
        {'name': 'Mario'},
        {'name': 'Link'},
        {'name': 'Donkey Kong'},
    }
    connection.execute(target.insert(), preloaded_sellers)


event.listen(Seller.__table__, 'after_create', insert_data)
