"""
    Author:          Hartmut Mathussek
    Date Created:    08/23/2020
    Functionality:
                     This module handles all the database stuff
                     
"""

import sqlite3
from sqlite3 import Error
from datetime import datetime

def func_create_connection(db_file):
    # Open connection to db
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        return conn

def func_close_db_connection(conn):
    # Close connection to db
    try:
        conn.close()
    except Error as e:
        print(e)
        
def func_create_table_stock_prices(conn):
    # Create stock_pricess table if it does not exist
    # Input: connection
    create_new_table = """ CREATE TABLE IF NOT EXISTS stock_prices (
                           symbol text NOT NULL,
                           date date NOT NULL,
                           open double NOT NULL,
                           high double NOT NULL,
                           low double NOT NULL,
                           close double NOT NULL,
                           volume double NOT NULL) """
    curs = conn.cursor()
    curs.execute(create_new_table)

def func_create_table_stocks(conn):
    # Create stocks table if it does not exist
    # Input: connection
    create_new_table = """ CREATE TABLE IF NOT EXISTS stocks (
                           stock_id integer PRIMARY_KEY,
                           investor_id integer NOT NULL,
                           symbol text NOT NULL,
                           no_shares integer NOT NULL,
                           purchase_price double NOT NULL,
                           current_value double NOT NULL,
                           purchase_date date NOT NULL,
                           min_win_notification NOT NULL,
                           low_price_warning NOT NULL) """
    curs = conn.cursor()
    curs.execute(create_new_table)

def func_create_table_bonds(conn):
    # Create bonds table if it does not exist
    # Input: connection
    create_new_table = """ CREATE TABLE IF NOT EXISTS bonds (
                           bond_id integer PRIMARY_KEY,
                           investor_id integer NOT NULL,
                           symbol text NOT NULL,
                           no_shares integer NOT NULL,
                           purchase_price double NOT NULL,
                           current_value double NOT NULL,
                           purchase_date date NOT NULL,
                           coupon double NOT NULL,
                           yield NOT NULL) """
    curs = conn.cursor()
    curs.execute(create_new_table)

def func_create_table_investors(conn):
    # Create investors table if it does not exist
    # Input: connection
    create_new_table = """ CREATE TABLE IF NOT EXISTS investors (
                           investor_id integer PRIMARY_KEY,
                           investor_name text NOT NULL,
                           investor_address text NOT NULL,
                           investor_phone text NOT NULL,
                           investor_email text NOT NULL) """
    curs = conn.cursor()
    curs.execute(create_new_table)


def func_execute_sql(sql_string, conn):
    # This function executes the sql statement that is passed in for the current connection
    # Input: sql statement to be executed
    # Input: connection object
    try:
        curs = conn.cursor()
        curs.execute(sql_string)
    except Error as e:
        print(e)

def func_return_results(sql_string, conn):
    # This function returns the results from an sql query
    # Input: sql statement to be executed
    # Input: connection object
    # Output: result rows
    try:
        curs = conn.cursor()
        curs.execute(sql_string)
        rows = curs.fetchall()
        return rows
    except Error as e:
        print(e)

def func_close_connection(conn):
    # Close connection to db
    # Input: connection
    try:
        conn.close()
    except Error as E:
        print(e)



                   



