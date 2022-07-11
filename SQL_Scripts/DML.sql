INSERT INTO departments_pr 
VALUES(1, "Electronics","Electronic items are stored in this department"),
	  (2,"Clothing","Clothing items are stored in this department"),
	  (3, "Toys","Toy items are stored in this department"),
	  (4,"Baby","Baby care items are stored in this department");
SELECT * FROM departments_pr;

INSERT INTO products_pr
VALUES(5,"Laptop", 2500, "Intel i7 processor 16 GB RAM", 1),
	  (6, "tees", 10, "Calvin Klein", 2),
      (7, "Escavator", 25, "Hot Wheels", 3),
      (8, "Baby lotion", 12.5, "Johnson baby lotion", 4);
SELECT * FROM products_pr;

INSERT INTO customers_pr
VALUES(100, "Felix", "Kucukgokmen", "felixkucukgokmen", "felix", "felix@gmail.com"),
      (101, "Vanessa", "Kwende", "vanessakwende", "vanessa", "vanessa@gmail.com"),
      (102, "Leena", "Varghese", "leenavarghese", "leena", "leena@gmail.com");
      
INSERT INTO customers_pr
VALUES(103, "Dhvani", "Pandya", "dhvanipandya", "dhvani", "dhvani@gmail.com");
SELECT * FROM customers_pr;

INSERT INTO addresses_pr
VALUES(1000, "Unit 123", "London", "ON", "NH61D3", 100),
      (1001,"Unit 11", "Brampton", "ON", "M5F2D9", 101),
	  (1002, "Unit 567", "Mississauga", "ON", "L5V1H4", 102); 
SELECT * FROM addresses_pr;

INSERT INTO orders_pr
VALUES(1101, 3750, '2021-10-01', 122.5, 102),
      (1102, 7450, '2020-01-20', 872.5, 101);
SELECT * FROM orders_pr;

