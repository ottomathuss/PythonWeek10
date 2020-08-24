"""
    Author:          Hartmut Mathussek
    Date Created:    08/23/2020
    Functionality:
                     This program reads stock and bond information and saves it in a database.
                     It then reads closing prices from a json file and saves those to the databse.
                     It then creates a chart of the value of each stock over time.
                     Finally, it compares current stock prices with threshold levels and sends out
                     emails if thresholds are exceeded
"""

import class_stocks
import mod_db
import mod_email
import sys
import os
import pandas as pd
import csv
from csv import reader
import json
import matplotlib.pyplot as plt
from datetime import datetime

# Open csv files
try:
    # Read stock data into dataframe
    df_stocks = pd.read_csv('Lesson6_Data_Stocks.csv', delimiter=',')
    stock_tuples = [tuple(row) for row in df_stocks.values]

    # Create lists of stock headers
    with open('Lesson6_Data_Stocks.csv', 'r') as headerrow:
        d_stock_reader = csv.DictReader(headerrow)
        stock_headers = d_stock_reader.fieldnames

    # Read bond data into dataframe
    df_bonds = pd.read_csv('Lesson6_Data_Bonds.csv', delimiter=',')
    bond_tuples = [tuple(row) for row in df_bonds.values]

    # Create lists of stock headers
    with open('Lesson6_Data_Bonds.csv', 'r') as headerrow:
        d_bond_reader = csv.DictReader(headerrow)
        bond_headers = d_bond_reader.fieldnames

except:
    # If any of the specified files does not exist, exit progam
    print("The specified file does not exist.")
    sys.exit()

# Create/open database and return connection object
db_path = os.path.dirname(os.path.realpath(__file__))
conn = mod_db.func_create_connection(db_path + "\Stocks_Info.db")

# Create tables
mod_db.func_create_table_investors(conn)
mod_db.func_create_table_stocks(conn)
mod_db.func_create_table_bonds(conn)
mod_db.func_create_table_stock_prices(conn)

# Insert data into investors table
investorid = 1
try:
    sql_insert_investors = """Insert into investors (INVESTOR_ID, INVESTOR_NAME, INVESTOR_ADDRESS, INVESTOR_PHONE, INVESTOR_EMAIL) """ +\
                       """ values(""" + str(investorid) + """, 'Bob Smith', '123 Desert Road, Acme, NV 12345', '702-444-5555', 'otto_mathuss@comcast.net')"""
    mod_db.func_execute_sql(sql_insert_investors, conn)
except:
    print("Error reading investors")

# Insert data into stocks table
stockid = 1
try:
    for item in stock_tuples:
        sql_insert_stocks = """Insert into stocks (STOCK_ID, INVESTOR_ID, SYMBOL, NO_SHARES, PURCHASE_PRICE, CURRENT_VALUE, PURCHASE_DATE, MIN_WIN_NOTIFICATION, LOW_PRICE_WARNING) """ +\
            """ values(""" + str(stockid) + """, """ + str(investorid) + """, '""" + str(item[0]) + """', """ + str(item[1]) + """, """ + str(item[2]) + """, """ +\
            str(item[3]) + """, '""" + str(item[4]) + """', """ + str(item[5]) + """, """ + str(item[6]) + """)"""
        mod_db.func_execute_sql(sql_insert_stocks, conn)
        stockid +=1
except:
    print("Error reading stock information")

# Insert data into bonds table
bondid = 1
try:
    for item in bond_tuples:
        sql_insert_bonds = """Insert into bonds (BOND_ID, INVESTOR_ID, SYMBOL, NO_SHARES, PURCHASE_PRICE, CURRENT_VALUE, PURCHASE_DATE, COUPON, YIELD) """ +\
            """ values(""" + str(stockid) + """, """ + str(investorid) + """, '""" + str(item[0]) + """', """ + str(item[1]) + """, """ + str(item[2]) + """, """ +\
            str(item[3]) + """, '""" + str(item[4]) + """', """ + str(item[5]) + """, """ + str(item[6]) + """)"""
        mod_db.func_execute_sql(sql_insert_bonds, conn)
        bondid +=1
except:
    print("Error reading bond information")


# Open json file to see stock performance over time
file = "AllStocks-2.json"
try:
    with open (file) as json_file:
        data_set = json.load(json_file)

        # Insert data into stock_prices table
        for item in data_set:
            date1 = datetime.strptime(item['Date'], '%d-%b-%y')
            sql_insert_stock_prices = """Insert into stock_prices (SYMBOL, DATE, OPEN, HIGH, LOW, CLOSE, VOLUME) """ +\
                """ values('""" + str(item['Symbol']) + """', '""" + str(date1) + """', '""" + str(item['Open']) + """', '""" +\
                str(item['High']) + """', '""" + str(item['Low']) + """', '""" + str(item['Close']) + """', '""" + str(item['Volume']) + """')"""
            mod_db.func_execute_sql(sql_insert_stock_prices, conn)
except:
    print("Error reading json file with stock history information")
             
# Find all dates and put in list
sql_dates = "Select date, close, symbol from stock_prices order by symbol, date asc"
rows_dates = mod_db.func_return_results(sql_dates, conn)

list_dates = []
list_close = []
list_symbol = []

for date in rows_dates:
    # Write dates, closing prices and symbols to lists
    list_dates.append(datetime.strptime(date[0], '%Y-%m-%d %H:%M:%S'))
    list_close.append(date[1])
    list_symbol.append(str(date[2]))

list_close1 = []
list_date1 = []

# Get al stocks, purchase date and number of shares for investor
sql_stocks_owned = "Select symbol, no_shares, purchase_date from stocks"
rows_stocks_owned = mod_db.func_return_results(sql_stocks_owned, conn)

# Create subplot for each stock in investor's portfolio
for stock_owned in rows_stocks_owned:
    for count in range(0, len(list_symbol) -1):
        if list_symbol[count] == stock_owned[0]:
            list_date1.append(list_dates[count])
            if list_dates[count] > datetime.strptime(stock_owned[2], '%m/%d/%Y'):
                list_close1.append(list_close[count] * stock_owned[1])
            else:
               list_close1.append(0)
                
    plt.plot(list_date1, list_close1, label=stock_owned[0])
    list_date1 = []
    list_close1 = []

# Create plot
try:
    plt.title('Portfolio value over time')
    plt.xlabel('Dates')
    plt.ylabel('Portolio Value')
    plt.legend(loc="upper left")
    plt.show()
except:
    print("Error plotting data")

# Create notifications for investers about their stock performance
# Find all investors in investors table
sql_investors_notification = "Select investor_id, investor_email, investor_name from investors"
rows_investors = mod_db.func_return_results(sql_investors_notification, conn)

for investors in rows_investors:

    # Check if notification is necessary by looking at thresholds in Stocks table
    sql_today = "Select investor_id, symbol, no_shares, purchase_price, current_value, min_win_notification,low_price_warning from stocks where investor_id = " + str(investors[0])
    rows_today = mod_db.func_return_results(sql_today, conn)

    notification = """Hello """ + investors[2] + """,\n\nThis is an automated message from your Stock program. The following requires your attention:\n\n"""
    warning = "No"
    warning_notification = ""
    winning = "No"
    winning_notification = ""

    for stocks in rows_today:
        # Find threshold values in stocks table
        current_winnings = (stocks[4] - stocks[3]) * stocks[2]
        if stocks[4] < stocks[6]:
            warning_notification = warning_notification + stocks[1] + """: The current price of """ + str(stocks[4]) + """ is lower than your warning threshold of """ + str(stocks[6]) + """\n"""
            warning = "Yes"
        elif current_winnings > stocks[5]:
            winning_notification = winning_notification + stocks[1] + """: You currently made a profit of """ + str(format(current_winnings, ",.2f")) + """ on this stock!\n"""
            winning = "Yes"

    if warning == "No":
        warning_notification = """Warnings issued: None!"""
    else:
        warning_notification = """The following warnings have been issued:\n\n""" + warning_notification

    notification = notification + warning_notification + """\n"""

    if winning == "No":
        winning_notification = """Winning thresholds exceeded: None!"""
    else:
        winning_notification = """The following stocks outperform your expections:\n\n""" + winning_notification

    notification = notification + winning_notification + """\nPlease take the appropriate action.\n\nSincerly,\n\nYour Stock Program"""

    # Send message to current investor
    result = mod_email.f_smtp_server(notification, investors[1])
    print(result)
   
# Close connection to database
mod_db.func_close_connection(conn)

print("End of program")

