-- Create schema
CREATE DATABASE restaurant;

--Table Menu_card
CREATE TABLE restaurant.Menu_card (
    menu_id INT PRIMARY KEY,
    Menu VARCHAR(100),
    Price FLOAT,
    Available CHAR(1) CHECK (Available IN ('Y', 'N'))
);

-- Create Table Order
CREATE TABLE restaurant.placed_order (
    sr_no INT PRIMARY KEY IDENTITY(1,1),
    tbl_id INT,
    menu_id INT,
    quantity INT,
    order_date DATETIME,
    FOREIGN KEY (menu_id) REFERENCES restaurant.Menu_card(menu_id),
    UNIQUE (tbl_id, menu_id, order_date)
);

-- Create Table Final_bill
CREATE TABLE restaurant.Final_bill (
    bill_id VARCHAR(50) UNIQUE,
    bill_date DATETIME,
    tbl_id INT,
    total_amount FLOAT,
    gst_charges FLOAT,
    final_amount FLOAT,
    UNIQUE (bill_id, bill_date, tbl_id)
);

INSERT INTO restaurant.Menu_card (menu_id, Menu, Price, Available) VALUES
(1, 'Vada', 30.0, 'Y'),
(2, 'Idli', 20.0, 'Y'),
(3, 'Dosa', 50.0, 'Y'),
(4, 'Puri Bhaji', 40.0, 'N'),
(5, 'Uttapam', 45.0, 'Y'),
(6, 'Pongal', 55.0, 'Y'),
(7, 'Masala Dosa', 60.0, 'Y'),
(8, 'Medu Vada', 25.0, 'N'),
(9, 'Sambar Rice', 70.0, 'Y'),
(10, 'Curd Rice', 65.0, 'Y'),
(11, 'Upma', 35.0, 'Y'),
(12, 'Poori', 30.0, 'N'),
(13, 'Chapati', 20.0, 'Y'),
(14, 'Paneer Dosa', 75.0, 'Y'),
(15, 'Cheese Dosa', 80.0, 'Y'),
(16, 'Ghee Roast', 85.0, 'Y'),
(17, 'Kesari Bath', 50.0, 'N'),
(18, 'Lemon Rice', 60.0, 'Y'),
(19, 'Bisi Bele Bath', 90.0, 'Y'),
(20, 'Rava Idli', 40.0, 'Y');


select * from restaurant.Menu_card;
select * from restaurant.placed_order;
select * from restaurant.Final_bill;