# Swiss Pairings Tournament

The purpose of this project is to utilize both relational databases and python
to generate results of a Swiss Pairing tournament.

This was prepared as part of Udacity's Introduction to Relational Databases
course.

## Necessary Files
1.  **Udacity's fullstack-nanodegree-vm** - Original version can be obtained
from the following
Github link:  https://github.com/udacity/fullstack-nanodegree-vm.git.  This
directory contains the necessary Vagrant and VirtualBox programs used to run the
databases.
2.  **Tournament** Folder
  1.  **tournament.py** - Python file containing the primary Python code needed to run the tournament functions (e.g. registering players, generating standings, determining the next pairing, etc.).  This code contains the Postgresql queries.
  2.  **tournament.sql** - Contains the SQL to setup the tables for the tournament.  Also contains the schema for the views used to aggregate match results.
  3.  **tournament_test.py** - Contains Udacity's test functions used to test the basic functionality of tournament.py.

## Dependencies
- Programs must be run with Vagrant running and logged in.  

## Limitations
- swissPairings() currently only supports an even number of players.

## Getting Started
-  Navigate to the vagrant folder and enter "vagrant up" in the command line to boot the virtual machine.
- Enter "vagrant ssh" in the command line to login to the virtual machine.
- Type "cd /vagrant/tournament" into the command line to navigate to the tournament folder in the virtual machine.
- Once in the tournament directory you can run tournament_test.py to verify the functionality of the python.py.
- To register players and enter results for finished round, review each function and provide the necessary inputs.

- To access the database type "psql" into the command line.  Then type \c tournament to connect to the tournament database.  You should see "tournament=>" at the start of the command line.  This indicates that you are connected to the database.  From here you can query or write to the tournament database.
