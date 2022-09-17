from models import Base, SalesTable, Seller
from settings import db_conn_str
from sqlalchemy.orm import sessionmaker
import logging
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

logging.basicConfig(format='[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


def check_item_price() -> object:
    is_price_number = False
    while not is_price_number:
        try:
            sale_item_value = float(input('Item Price: $'))
            return sale_item_value
        except ValueError as e:
            logging.error('Item price was not valid number!')
            print()


class SalesManager:
    db_session = None
    is_running = False

    def connect_on_db(self):
        logging.warning('Trying conecting on Database...')
        try:
            engine = create_engine(db_conn_str)
            Base.metadata.create_all(engine)
            session = sessionmaker(bind=engine)
            self.db_session = session()
            self.is_running = True
            logging.warning('Successful connection!')
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'].args[1])
            logging.error(f'Error on connection: {error}')
        print()

    def check_seller_name(self) -> object:
        has_seller = False
        while not has_seller:
            seller_name = input('Seller Name: ')
            seller = self.db_session.query(Seller).filter_by(name=seller_name.lower()).all()
            if seller:
                return seller[0]
            logging.error('Seller not found!')
            print()

    def make_sale(self):
        seller = self.check_seller_name()
        customer_name = input('Customer Name: ')
        sale_item_name = input('Item Name: ')
        sale_item_value = check_item_price()

        sale = SalesTable(
            seller=seller.id,
            customer_name=customer_name,
            sale_item_name=sale_item_name,
            sale_item_value=sale_item_value
        )
        self.db_session.add(sale)
        self.db_session.commit()

        should_close = input('\nPress any key to continue or write "exit" to close the manager: ')
        if should_close.lower() == 'exit':
            self.is_running = False
