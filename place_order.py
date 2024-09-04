"""
This script handles placing orders at a restaurant and 
generating a bill for a specific table.
"""
from bill_generator import Restaurant

# Object creation
restaurant = Restaurant(tbl_id=12)

# Place orders
first_order = restaurant.place_order(menu_id=5, quantity=2)
second_order = restaurant.place_order(menu_id=6, quantity=3)

if first_order or second_order:
# Generate the bill
    restaurant.generate_bill()
else:
    print("There is unavailability of ordered items.")
