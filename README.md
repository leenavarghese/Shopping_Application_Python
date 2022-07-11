## ABOUT THE PROJECT
This is a shopping application that allows customers to search products, add new items, display the products, and order products. The application is integrated with a database in MySQL with a schema of 6 tables. Create account option registers customers using customers’ first name, last name, user name, password and unique identifier. Email ID is used as unique identifier. Every email address is unique so customer information is added to the system using unique identifier which is Email ID. Before a customer is registered, system checks to see if this customer is not already registered in the system. An already existing user  can login using his email id and password. Once the customer successfully logs in(for existing user) or create a new account(for new users), he is presented with the welcome page. For an existing user who has made orders in the past, he can know the details of his order by choosing the search order option. If the order id exists, the details of the order are displayed. A scroll bar is provided so as to easily navigate is case of multiple entries. Next, the user can choose between 4 departments- Electronics, Toys, Clothing and Baby products. This gives the customer an option to choose a product from the drop-down menu which lists the products available in that category and the customer can chose the quantity of items. When Checkout button is selected the screen with options to enter his address is displayed and thus he can successfully place the order.

## TECHNOLOGY STACK AND TOOLS USED
* Python
* MySQL
* PyCharm
* MySQL Workbench

## ER DIAGRAM
![Entity Relationship Diagram](/images/ER%20diagram.PNG)