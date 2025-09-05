# Shopping List

## Application Features
*  Users can create an account and log in to the application.
*  Users can create a shopping list that is protected by a password.
*  Users can search for and join another user's shopping list if they know the list name and password.
*  Users can add products to the shopping list, specify the required quantity, and edit or delete the products they have added.
*  Users can assign a category to each product (Groceries, Household Items, Other).
*  Users can see all products added to the shopping list, including their own and those added by other users.
*  Users can assign any member of the list as the buyer for a product. Based on this assignment, the product will appear on the buyer’s user page.
*  The user page shows purchase information:
*  Price, quantity, and purchase time of the products paid for by the user.
*  If the list has multiple members, the user’s share of purchases is automatically calculated as a percentage of all users’ purchases.
*  Each list has its own user pages, so purchased products are not mixed between different lists.
*  When the last user leaves a list, all information related to that list is removed from the database. The application confirms with the user before performing this action.
*  The shopping list can be sorted by product categories.

## Application installation

## Create a virtual environment
python3 -m venv venv

## Activate the virtual environment
source venv/bin/activate

## Install Flask
pip install flask

## Create the database tables and initial data
sqlite3 database.db < schema.sql
sqlite3 database.db < init.sql

## Run the application
flask run