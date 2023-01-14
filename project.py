"""CSC 161 Project: Milestone III

Xuchen Huang
Lab Section TR 6:15-7:30pm
Spring 2021
"""


def test_data(filename, col, day):
    """A test function to query the data you loaded into your program.

    Args:
        filename: A string for the filename containing the stock data,
                  in CSV format.

        col: A string of either "date", "open", "high", "low", "close",
             "volume", or "adj_close" for the column of stock market data to
             look into.

             The string arguments MUST be LOWERCASE!

        day: An integer reflecting the absolute number of the day in the
             data to look up, e.g. day 1, 15, or 1200 is row 1, 15, or 1200
             in the file.

    Returns:
        A value selected for the stock on some particular day, in some
        column col. The returned value *must* be of the appropriate type,
        such as float, int or str.
    """
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    headers = ["date", "open", "high", "low", "close", "adj_close", "volume"]
    for i in range(len(headers)):
        if col == headers[i].lower():
            j = day
            linej = lines[j]
            vals = linej.split(",")
            val = vals[i]
    if col == "date":
        return val
    elif col in ["open", "high", "low", "close", "adj_close"]:
        return float(val)
    elif col == "volume":
        return int(val)

    
def transact(funds, stocks, qty, price, buy=False, sell=False):
    """A bookkeeping function to help make stock transactions.

       Args:
           funds: An account balance, a float; it is a value of how much money
           you have, currently.

           stocks: An int, representing the number of stock you currently own.

           qty: An int, representing how many stock you wish to buy or sell.

           price: An float reflecting a price of a single stock.

           buy: This option parameter, if set to true, will initiate a buy.

           sell: This option parameter, if set to true, will initiate a sell.

       Returns:
           Two values *must* be returned. The first (a float) is the new
           account balance (funds) as the transaction is completed. The second
           is the number of stock now owned (an int) after the transaction is
           complete.

           Error condition #1: If the `buy` and `sell` keyword parameters
           are both set to true, or both false. You *must* raise an
           ValueError exception with an appropriate error message since this
           is an ambiguous transaction.

           Error condition #2: If you buy, or sell without enough funds or
           stocks to sell, respectively.  You *must* raise an
           ValueError exception with an appropriate error message since this
           is an ambiguous transaction.
    """
    if buy is True and sell is False:
        if funds < qty * price:
            raise ValueError(f"Insufficient funds to purchase {qty} stock at ${price:0.2f}!")
        else:
            curfund = funds - qty * price
            curstock = stocks + qty
            return float(curfund), int(curstock)
    elif buy is False and sell is True:
        if stocks < qty:
            raise ValueError(f"Insufficient stock owned to sell {qty} stocks!")
        else:
            curfund = funds + qty * price
            curstock = stocks - qty
            return float(curfund), int(curstock)
    else:
        raise ValueError("Ambiguous transaction! Can't determine whether to buy or sell!")


def alg_moving_average(filename):
    """This function implements the moving average stock trading algorithm.

    The CSV stock data should be loaded into your program; use that data to
    make decisions using the moving average algorithm.

    Any bookkeeping setup from Milestone I should be called/used here.

    Algorithm:
    - Trading must start on day 21, taking the average of the previous 20 days.
    - You must buy shares if the current day price is 5%, or more, lower
      than the moving average.
    - You must sell shares if the current day price is 5%, or more, higher,
      than the moving average.
    - You must buy, or sell 10 stocks, or less per transaction.
    - You are free to choose which column of stock data to use (open, close,
      low, high, etc)
    - When your algorithm reaches the last day of data, have it sell all
      remaining stock. Your function will return the number of stocks you
      own (should be zero, at this point), and your cash balance.
    - Choose any stock price column you wish for a particular day you use
      (whether it's the current day's "open", "close", "high", etc)

    Args:
        A filename, as a string.

    Returns:
        Note: You *must* sell all your stock before returning.
        Two values, stocks and balance OF THE APPROPRIATE DATA TYPE.

    Prints:
        Nothing.
    """

    # Last thing to do, return two values: one for the number of stocks you end up
    # owning after the simulation, and the amount of money you have after the simulation.
    # Remember, all your stocks should be sold at the end!
    stocks_owned = 0
    cash_balance = 1000
    open_values = []
    current_average = 0
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    del lines[0]
    for i in range(len(lines)):
        linei = lines[i]
        vals = linei.split(',')
        open_values.append(float(vals[1]))
    for i in range(len(open_values)):
        if i >= 20:
            current_average = sum(open_values[i-20: i]) / 20
            cp = open_values[i]
            if current_average <= 0.95 * cp and 10 * cp <= cash_balance:
                cash_balance, stocks_owned = transact(
                    cash_balance, stocks_owned, 10, cp, True, False)
            elif current_average >= 1.05 * cp and 10 <= stocks_owned:
                cash_balance, stocks_owned = transact(
                    cash_balance, stocks_owned, 10, cp, False, True)
        if i == len(open_values) - 1:
            cash_balance, stocks_owned = transact(
                cash_balance, stocks_owned, stocks_owned, cp, False, True) 
    return stocks_owned, cash_balance


def cal_RSI(filename):
    Lookback = 14
    totalG = 0
    totalL = 0
    open_values = []
    RSI = []
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    del lines[0]
    for i in range(len(lines)):
        linei = lines[i]
        vals = linei.split(',')
        open_values.append(float(vals[1]))
    for i in range(len(open_values)):
        if i >= Lookback:
            if open_values[i - 13] > open_values[i - 14]:
                gains = open_values[i - 13] - open_values[i - 14]
                totalG = totalG + gains
            else:
                gains = 0
                totalG = totalG + gains
            averageG = totalG / Lookback
            if open_values[i - 13] < open_values[i - 14]:
                losses = open_values[i - 14] - open_values[i - 13]
                totalL = totalL + losses
            else:
                losses = 0
                totalL = totalL + losses
            averageL = totalL / Lookback
            if averageL != 0:
                rsi = 100 - (100 / (1 + (averageG / averageL)))
                RSI.append(rsi)
    return RSI


def read_file(filename):
    open_values = []
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    del lines[0]
    for i in range(len(lines)):
        linei = lines[i]
        vals = linei.split(',')
        open_values.append(float(vals[1]))
    return open_values

    
def alg_rsi(filename_1, filename_2):
    """This function implements the Relative Strength Index algorithm.

    Using the CSV stock data from two stock files that are loaded into your
    program, use that data to make decisions using the Relative Strength
    Index (RSI) algorithm.

    Algorithm:
    - Trading must start on day 15, calculate RSI based
      on the 14 days looking back period.
    - If average loss is 0, ignore the RSI value
    - You must buy shares if the RSI of a stock is less than 30
    - You must sell shares if the RSI of a stock is larger than 70
    - You must buy, or sell 10 stocks, or less per transaction.
    - You are free to choose which column of stock data to use (open, close,
      low, high, etc)
    - You must calculate cash balance and stock owned for
      the two skocks seperately
      from day 15 to the day before the last day.
    - When your algorithm reaches the last day of data, have it sell all
      remaining stock. In this step you calculate the total
      cash balance and stock
      owned by merging the cash balance and stock owned
      of the two stocks together.
      Your function will return the number of stocks you
      own (should be zero, at this point), and your cash balance.
    - Choose any stock price column you wish for a particular day you use
      (whether it's the current day's "open", "close", "high", etc)

    Arguments:
        filename_1 (str): A filename, as a string, for one set of stock
                          data for a first company.

        filename_2 (str): A filename, as a string, for one set of stock
                          data for a second company.

    Returns:
        Two values, stocks and balance OF THE APPROPRIATE DATA TYPE.

    Prints:
        Nothing.
    """

    # Last thing to do, return two values: one for the number of stocks you
    # end up owning after the simulation, and the amount of money you have
    # after the simulation. Remember, all your stocks should be sold at the
    # end!
    stocks_owned1 = 0
    stocks_owned2 = 0
    cash_balance = 10000
    RSI1 = cal_RSI(filename_1)
    RSI2 = cal_RSI(filename_2)
    opvalues1 = read_file(filename_1)
    opvalues2 = read_file(filename_2)
    for j in range(14, len(opvalues1) - 1):
        #if j >= 14:
            cp1 = opvalues1[j]
            for a in RSI1:
                if a < 30 and 10 * cp1 <= cash_balance:
                    cash_balance, stocks_owned1 = transact(
                        cash_balance, stocks_owned1, 10, cp1, True, False)
                elif a > 70 and 10 <= stocks_owned1:
                    cash_balance, stocks_owned1 = transact(
                        cash_balance, stocks_owned1, 10, cp1, False, True)
    for k in range(len(opvalues2) - 1):
        #if k >= 14:
            cp2 = opvalues2[k]
            for b in RSI2:
                if b < 30 and 10 * cp2 <= cash_balance:
                    cash_balance, stocks_owned2 = transact(
                        cash_balance, stocks_owned2, 10, cp2, True, False)
                elif b > 70 and 10 <= stocks_owned2:
                    cash_balance, stocks_owned2 = transact(
                        cash_balance, stocks_owned2, 10, cp2, False, True)
    cash_balance, stocks_owned = transact(
        cash_balance, stocks_owned1, stocks_owned1, opvalues1[-1], False, True)
    cash_balance, stocks_owned = transact(
        cash_balance, stocks_owned2, stocks_owned2, opvalues2[-1], False, True)
    return stocks_owned, cash_balance


# Don't forget the required "__main__" check!
def main():
    # My testing will use AAPL.csv or MSFT.csv
    stock_file_1 = input("Enter a filename for stock data (in CSV format): ")

    # Call your moving average algorithm, with the filename to open.
    alg1_stocks, alg1_balance = alg_moving_average(stock_file_1)

    # Print results of the moving average algorithm, returned above:
    print("The results are ", alg1_stocks, alg1_balance)

    # Now, call your RSI algorithm!
    stock_file_2 = input("Enter another filename for second"
                         "stock data file (in CSV format): ")
    alg2_stocks, alg2_balance = alg_rsi(stock_file_1, stock_file_2)

    # Print results of your algorithm, returned above:
    print("The results are ", alg2_stocks, alg2_balance)


if __name__ == '__main__':
    main()
