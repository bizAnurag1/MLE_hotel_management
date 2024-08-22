from bill_generator import *

# Object creation
restaurant = Restaurant(tbl_id=11)

# Place orders
order1 = restaurant.place_order(menu_id=5, quantity=2)
order2 = restaurant.place_order(menu_id=6, quantity=3)

if order1 or order2:
# Generate the bill
    restaurant.generate_bill()
else:
    print("There is unavailability of ordered items.")
