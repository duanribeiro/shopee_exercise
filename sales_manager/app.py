from helpers import SalesManager

if __name__ == '__main__':
    manager = SalesManager()
    manager.connect_on_db()

    while manager.is_running:
        manager.make_sale()
