import pyodbc
import datetime
from contextlib import contextmanager

@contextmanager
def db_connection():
    conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=DESKTOP-OLPAHOD\\SQLEXPRESS;'
    'DATABASE=Restaurant;'
    'Trusted_Connection=yes;'
    )
    try:
        yield conn.cursor()
    finally:
        conn.commit()
        conn.close()

@contextmanager
def log_entry(action):
    with open("order_log.txt", "a") as log_file:
        log_file.write(f"{datetime.datetime.now()}: {action}\n")
    yield

# Order and Billing System
class Restaurant:
    def __init__(self, tbl_id):
        self.tbl_id = tbl_id

    def check_menu_availability(self, menu_id):
        with db_connection() as conn:
            available = conn.execute("SELECT Available FROM restaurant.Menu_card WHERE menu_id = ?", 
                                     (menu_id,)).fetchone()
            return available and available[0] == 'Y'

    def place_order(self, menu_id, quantity):
        if self.check_menu_availability(menu_id):
            order_date = datetime.datetime.now()

            with db_connection() as conn:
                conn.execute("""
                    INSERT INTO restaurant.placed_order (tbl_id, menu_id, quantity, order_date)
                    VALUES (?, ?, ?, ?)
                """, (self.tbl_id, menu_id, quantity, order_date))

            with log_entry(f"Order placed: Table {self.tbl_id}, Menu {menu_id}, Quantity {quantity}"):
                pass

            print(f"Order placed successfully for Table {self.tbl_id}.")
            return True
        else:
            print("Menu item is not available.")
            with log_entry(f"Failed order attempt: Table {self.tbl_id}, Menu {menu_id} is unavailable"):
                pass
            return False

    def calculate_bill(self):
        bill_date = datetime.datetime.now()

        with db_connection() as conn:
            orders = conn.execute("""
                SELECT M.Menu, O.quantity, M.Price 
                FROM restaurant.placed_order O 
                JOIN restaurant.Menu_card M 
                ON O.menu_id = M.menu_id 
                WHERE O.tbl_id = ? 
                AND O.order_date BETWEEN ? AND ?
            """, (self.tbl_id, bill_date.replace(hour=0, minute=0, second=0, microsecond=0), bill_date)).fetchall()

        total_amount = sum([quantity * price for _, quantity, price in orders])
        gst_charges = total_amount * 0.1
        final_amount = total_amount + gst_charges

        bill_id = f"Bill_{self.tbl_id}_{int(bill_date.timestamp())}"

        with db_connection() as conn:
            conn.execute("""
                INSERT INTO restaurant.Final_bill (bill_id, bill_date, tbl_id, total_amount, gst_charges, final_amount)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (bill_id, bill_date, self.tbl_id, total_amount, gst_charges, final_amount))

        with log_entry(f"Bill generated: {bill_id} for Table {self.tbl_id} with final amount {final_amount}"):
            pass

        return {
            'bill_id': bill_id,
            'bill_date': bill_date,
            'orders': orders,
            'total_amount': total_amount,
            'gst_charges': gst_charges,
            'final_amount': final_amount
        }

    def generate_bill(self):
        bill_data = self.calculate_bill()

        print("-"*40)
        print("|          Welcome to Hotel Annapurna          |")
        print(f"|{bill_data['bill_date'].strftime('%Y-%m-%d')}       recpt: {bill_data['bill_id']}|")
        print("-"*40)
        print("|SR.    Menu           qnt     price   |")

        for i, (menu, quantity, price) in enumerate(bill_data['orders'], start=1):
            print(f"|{i}   {menu}      {quantity}     {quantity * price}        |")

        print("-"*40)
        print(f"|Total amount      =     {bill_data['total_amount']}     |")
        print(f"|including GST 10% =     {bill_data['gst_charges']}      |")
        print(f"|Final amount      =     {bill_data['final_amount']}     |")
        print("-"*40)
