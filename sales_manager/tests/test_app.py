from sqlalchemy.orm import scoped_session, sessionmaker
import pytest
from sales_manager.models import SalesTable, Seller
from sales_manager.settings import db_conn_str
from sqlalchemy import create_engine, func


@pytest.fixture(scope='session')
def db_engine(request):
    """yields a SQLAlchemy engine which is suppressed after the test session"""
    engine_ = create_engine(db_conn_str, echo=True)

    yield engine_

    engine_.dispose()


@pytest.fixture(scope='session')
def db_session_factory(db_engine):
    """returns a SQLAlchemy scoped session factory"""
    return scoped_session(sessionmaker(bind=db_engine))


@pytest.fixture(scope='function')
def db_session(db_session_factory):
    """yields a SQLAlchemy connection which is rollbacked after the test"""
    session_ = db_session_factory()
    session_.query(SalesTable).delete()

    yield session_

    session_.rollback()
    session_.close()


def test_sale(db_session):
    """Test a single sale"""
    sale = SalesTable(
        seller=1,
        customer_name='customer_name',
        sale_item_name='sale_item_name',
        sale_item_value=123
    )

    db_session.add(sale)
    db_session.commit()

    result = db_session.query(SalesTable).one()
    assert sale == result


def test_sorting(db_session):
    """Test show all sales in order"""
    sale1 = SalesTable(
        seller=1,
        customer_name='customer_name_1',
        sale_item_name='sale_item_name_1',
        sale_item_value=1
    )
    sale2 = SalesTable(
        seller=2,
        customer_name='customer_name_2',
        sale_item_name='sale_item_name_2',
        sale_item_value=2
    )
    db_session.add(sale1)
    db_session.add(sale2)
    db_session.commit()

    result = db_session.query(
            Seller.name, func.sum(SalesTable.sale_item_value).label("total_sales")
        ).join(
            Seller
        ).group_by(
            SalesTable.seller
        ).order_by(
            func.sum(SalesTable.sale_item_value).desc()
        ).all()

    expected = [
        ('lara croft', 2.0),
        ('cloud strife', 1.0)
    ]
    assert expected == result