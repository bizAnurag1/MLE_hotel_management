"""
This module defines a Restaurant class that provides an order and billing system for a restaurant.
It allows checking menu item availability, placing orders, and generating bills with GST calculation.
"""
import datetime
import logging
from contextlib import contextmanager
import pyodbc

logging.basicConfig(
    filename="order_log.txt",
    level=logging.INFO,
    format='%(asctime)s: %(levelname)s -- %(message)s'
)

@contextmanager
def db_connection():
    """
    Context manager for database connection using pyodbc.
    Yields:pyodbc.Cursor: A cursor object to execute SQL queries.
    """
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

# Order and Billing System
class Restaurant:
    """
    A class to represent a restaurant's order and billing system.
    Attributes: table_id (int): The ID of the table for which the orders and billing are managed.
    """
    def __init__(self, tbl_id):
        """
        Initializes a new instance of the Restaurant class.
        Args: table_id (int): The ID of the table for which orders and billing will be managed.
        """
        self.tbl_id = tbl_id

    def check_menu_availability(self, menu_id):
        """
        Checks if a menu item is available.
        Args: menu_id (int): The ID of the menu item to check for availability.
        Returns: bool: True if the menu item is available, False otherwise.
        """
        with db_connection() as conn:
            available = conn.execute("SELECT Available FROM restaurant.Menu_card WHERE menu_id = ?",
                                     (menu_id,)).fetchone()
            return available and available[0] == 'Y'

    def place_order(self, menu_id, quantity):
        """
        Places an order for a menu item if it is available.
        Args: menu_id (int): The ID of the menu item to order.
              quantity (int): The quantity of the menu item to order.
        Returns: bool: True if the order is placed successfully, False otherwise.
        """
        if self.check_menu_availability(menu_id):
            order_date = datetime.datetime.now()

            with db_connection() as conn:
                conn.execute("""
                    INSERT INTO restaurant.placed_order (tbl_id, menu_id, quantity, order_date)
                    VALUES (?, ?, ?, ?)
                """, (self.tbl_id, menu_id, quantity, order_date))

            logging.info("Order placed: Table %s, Menu %s, Quantity %s",self.tbl_id,menu_id,quantity)
            print(f"Order placed successfully for Table {self.tbl_id}.")
            return True
        else:
            logging.warning("Failed order attempt: Table %s, Menu %s is unavailable",self.tbl_id,menu_id)
            print("Menu item is not available.")
            return False

    def calculate_bill(self):
        """
        Calculates the bill for all orders placed at the table.
        Returns: dict: A dictionary containing bill details, including orders, total amount, 
                        GST charges, and final amount.
        """
        bill_date = datetime.datetime.now()

        with db_connection() as conn:
            orders = conn.execute("""
                SELECT M.Menu, O.quantity, M.Price 
                FROM restaurant.placed_order O 
                JOIN restaurant.Menu_card M 
                ON O.menu_id = M.menu_id 
                WHERE O.tbl_id = ? 
                AND O.order_date BETWEEN ? AND ?
            """,
            (self.tbl_id,bill_date.replace(hour=0,minute=0,second=0,microsecond=0),bill_date)).fetchall()

        total_amount = sum([quantity * price for _, quantity, price in orders])
        gst_charges = total_amount * 0.1
        final_amount = total_amount + gst_charges

        bill_id = f"Bill_{self.tbl_id}_{int(bill_date.timestamp())}"

        with db_connection() as conn:
            conn.execute("""
                INSERT INTO restaurant.Final_bill (bill_id, bill_date, tbl_id, total_amount, 
                         gst_charges, final_amount)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (bill_id, bill_date, self.tbl_id, total_amount, gst_charges, final_amount))

        logging.info("Bill: %s for Table %s with final amount %s",bill_id,self.tbl_id,final_amount)

        return {
            'bill_id': bill_id,
            'bill_date': bill_date,
            'orders': orders,
            'total_amount': total_amount,
            'gst_charges': gst_charges,
            'final_amount': final_amount
        }

    def generate_bill(self):
        """
        Generates and prints the bill for the table.
        The bill includes a list of all ordered items, their quantities, and prices, 
        as well as the total amount, GST charges, and the final amount to be paid.
        """
        bill_data = self.calculate_bill()

        print("-"*40)
        print("|          Welcome to Hotel Annapurna          |")
        print(f"|{bill_data['bill_date'].strftime('%Y-%m-%d')}      recpt: {bill_data['bill_id']}|")
        print("-"*40)
        print("|SR.    Menu           qnt     price   |")

        for i, (menu, quantity, price) in enumerate(bill_data['orders'], start=1):
            print(f"|{i}   {menu}      {quantity}     {quantity * price}        |")

        print("-"*40)
        print(f"|Total amount      =     {bill_data['total_amount']}     |")
        print(f"|including GST 10% =     {bill_data['gst_charges']}      |")
        print(f"|Final amount      =     {bill_data['final_amount']}     |")
        print("-"*40)
