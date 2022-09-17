from models import Base, SalesTable, Seller
from settings import engine
from sqlalchemy.orm import sessionmaker


def start_sales_manager() -> object:
    print('Starting sales manager system.')
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)

    return session()


def make_sale():
    seller_name = input('Seller Name: ')
    customer_name = input('Customer Name: ')
    sale_item_name = input('Item Name: ')
    sale_item_value = input('Item Price: ')
    # date = input('Date: ')

    return True