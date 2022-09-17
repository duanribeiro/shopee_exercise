from helpers import start_sales_manager, make_sale

if __name__ == '__main__':
    session = start_sales_manager()

    while session:
        make_sale()
