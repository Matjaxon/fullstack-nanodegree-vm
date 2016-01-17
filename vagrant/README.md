# Restaurant Web App Project

## Overview

The purpose of this project is to display basic web app development skills.

## Necessary Files
1.  **Udacity's fullstack-nanodegree-vm** - Original version can be obtained
from the following
Github link:  https://github.com/udacity/fullstack-nanodegree-vm.git.  This
directory contains the necessary Vagrant and VirtualBox programs used to run the
databases.

2.  **Catalog Folder**
  1.  **finalproject.py** - Python file containing the primary Python code needed to run the restaurant menu web app.  URL routing and SQLAlchemy queries are found here.
  2.  **restaurantmenu.db** - Database housing info on each restaurant and featured menu items.  CRUD functions in finalproject.py interact with this database.
  3.  **static folder** - Houses css files used for styling the application.
  4.  **templates folder** - Houses html templates for each webpage of the application.

## Dependencies
- Programs must be run with Vagrant running and logged in.

## Getting Started
- Navigate to the vagrant folder and enter "vagrant up" in the command line to boot the virtual machine.
- Enter "vagrant ssh" in the command line to login to the virtual machine.
- Type "cd /vagrant/catalog" into the command line to navigate to the catalog folder in the virtual machine.
- Once in the catalog directory you can run finalproject.py to verify the functionality of the application.
- The application will be running on local host 5000.
- Follow the links on each webpage to add, edit, or delete restaurants and items at each respective restaurant.
- Deleting a restaurant will delete all items associated with that restaurant from the database.
- All fields must be completed when creating or editing a restaurant or item.
- To access the database directly, type "psql" into the command line.  Then type \c restaurantmenu to connect to the restaurant database.  You should see "restaurantmenu=>" at the start of the command line.  This indicates that you are connected to the database.  From here you can query or write to the restaurantmenu database.
