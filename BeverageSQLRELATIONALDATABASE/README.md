# Overview

The Beverage Inventory 1.0 application is a very light, single-file Python program built to demonstrate practical use of a **SQL relational database** for inventory management. The goal of this project was to sshow how software interacts with structured operations such as inserting, updating, deleting, and retrieving records through SQL queries.

The software allows users to manage beverage stock by:
- Creating and viewing products in a local database  
- Adjusting quantities as inventory increases or decreases  
- Preventing invalid updates such as negative stock  
- Displaying results directly through a simple command-line interface  
- Summarizing data with aggregate functions

This project serves as a foundation for more advanced systems involving multi-table relationships, transaction tracking, and analytics.

To use the program:
1. Run `python pythonDBBev.py` from the command line.  
2. Follow the CLI menu to add products, adjust stock, or view data.  
3. The database (`inventory.db`) will be automatically created in the same directory as the script.

The purpose of this software is to exemplify how you can store inventory/stock in a relational database for easy inventory management, which is crucial when working with multiple people managing the same inventory.

[Software Demo Video](https://youtu.be/Cct2uf6-uW4)

Please note that on my video I misspoke on certain points, which I had prepared a few days ago (for example, one piece of the code I highlighted was using the product_id to specify which entry to remove, and NOT removing the product_id and consequently removing the rest of the data, which is what I mistakenly said.)

---

# Relational Database

The program uses **SQLite**, a lightweight, file-based relational database included with Python. SQLite provides full SQL support without requiring any external database server, making it perfect for quickly whipping up a prototype and testing locally.

### Database Structure

**Table: `products`**

| Column | Type | Description |
| `product_id` | INTEGER PRIMARY KEY AUTOINCREMENT | Unique identifier for each product |
| `product_name` | TEXT NOT NULL UNIQUE | Product name (must be unique; avoid using two products with the same name such as "cola") |
| `brand_name` | TEXT | Brand or manufacturer |
| `volume_ml` | INTEGER | Container size in milliliters |
| `stock_on_hand` | INTEGER NOT NULL DEFAULT 0 | Current quantity in stock |
| `created_at` | TEXT NOT NULL DEFAULT (datetime('now')) | Date and time when the product was added |

The `product_id` acts as the **primary key** for uniquely identifying each product.  
SQLite automatically handles ID assignment and enforces uniqueness and data integrity constraints.

# Development Environment

The project was developed in **Python 3.12** using VS Basic and command-line terminal. I did use SQLite3. 
No external dependencies were needed other than Python’s built-in libraries.

# Useful Websites

- [SQLite Tutorial](https://www.sqlitetutorial.net/)
- [Python sqlite3 Documentation](https://docs.python.org/3/library/sqlite3.html)
- [W3Schools SQL Reference](https://www.w3schools.com/sql/)
- [Real Python – Working with Databases in Python](https://realpython.com/python-sql-libraries/)

# Future Work

- Add an **`inventory_movements`** table to record restocks, sales, and returns using foreign keys; tracking this helps track issues & activity
- Iplement a sample automation that retrieves aggregate data to trigger a request to order more product
- Introduce a graphical or web-based UI for easier use  
- Include **data export** features (CSV or Excel) for reports  
