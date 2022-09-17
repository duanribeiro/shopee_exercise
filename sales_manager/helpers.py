from models import Base, SalesTable, Seller
from settings import db_conn_str
from sqlalchemy.orm import sessionmaker
import logging
from sqlalchemy import create_engine, func
from sqlalchemy.exc import SQLAlchemyError
from tabulate import tabulate

logging.basicConfig(format='[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


def check_item_price() -> float:
    """
    Creat a user input and check if the input is a number

    :return: input number as float
    """
    is_price_number = False
    while not is_price_number:
        try:
            sale_item_value = float(input('Item Price: $'))
            return sale_item_value
        except ValueError:
            logging.error('Item price was not valid number!')
            print()


class SalesManager:
    """
    SalesManager is the main class responsible to manage all operations

    :param db_session: The database session connection
    :param is_running: The flag reponsible for keep manager running
    """
    db_session = None
    is_running = False

    def connect_on_db(self):
        """
        Method to connect on MySQL database
        """
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

    def disconect_db(self):
        """
        Method to disconnect from MySQL database
        """
        self.db_session.close()
        self.is_running = False

    def check_seller_name(self) -> object:
        """
        Method to create a user input and check if the user exists on database

        :return: seller object from table
        """
        has_seller = False
        while not has_seller:
            seller_name = input('Seller Name: ')
            seller = self.db_session.query(Seller).filter_by(name=seller_name.lower()).all()
            if seller:
                return seller[0]
            logging.error('Seller not found!')
            print()

    def show_all_sales(self):
        """
        Method to show a list of all sales registered, sorted by sellers with the highest to lowest amount sold.
        """
        all_sales = self.db_session.query(
            Seller.name, func.sum(SalesTable.sale_item_value).label("total_sales")
        ).join(
            Seller
        ).group_by(
            SalesTable.seller
        ).order_by(
            func.sum(SalesTable.sale_item_value).desc()
        ).all()
        print(tabulate(all_sales, headers=['Name', 'Total Sales'], tablefmt="fancy_grid"))

    def make_sale(self):
        """
        Method to make a sale
        """
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

        self.show_all_sales()

        should_close = input('\nPress any key to continue or write "exit" to close the manager: ')
        print('--------------------------------------------------------------------')
        if should_close.lower() == 'exit':
            self.disconect_db()
