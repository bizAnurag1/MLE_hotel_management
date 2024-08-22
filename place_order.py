from bill_generator import *

# Object creation
restaurant = Restaurant(tbl_id=10)

# Place orders
order1 = restaurant.place_order(menu_id=4, quantity=2)
order2 = restaurant.place_order(menu_id=8, quantity=3)

if order1 or order2:
# Generate the bill
    restaurant.generate_bill()
else:
    print("There is unavailability of ordered items.")
