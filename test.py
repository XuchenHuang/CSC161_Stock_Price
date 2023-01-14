def test_data(filename, col, day):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    headline = lines[0]
    headers = headline.split(",")
    for i in range(len(headers)):
        if col == headers[i].lower():
            j = day
            linej = lines[j]
            vals = linej.split(",")
            val = vals[i]
    if col == "date":
        return val
    elif col in ["open", "high", "low", "close", "adj close"]:
        return float(val)
    elif col == "volume":
        return int(val)


def main():
    pass


if __name__ == '__main__':
    main()

for j in range(len(opvalues1)):
        for k in range(len(opvalues2)):
            if j >= 14 and k >= 14:
                cp1 = opvalues1[j]
                cp2 = opvalues2[k]
                for a in RSI1:
                    for b in RSI2:
                        if a < 30 and 10 * cp1 <= cash_balance:
                            cash_balance, stocks_owned = transact(
                                cash_balance, stocks_owned, 10, cp1, True, False)
                            if  b < 30 and 10 * cp2 <= cash_balance:
                                cash_balance, stocks_owned = transact(
                                    cash_balance, stocks_owned, 10, cp2, True, False)
                            elif b > 70 and 10 <= stocks_owned:
                                cash_balance, stocks_owned = transact(
                                    cash_balance, stocks_owned, 10, cp2, False, True)
                        elif a > 70 and 10 <= stocks_owned:
                            cash_balance, stocks_owned = transact(
                                cash_balance, stocks_owned, 10, cp1, False, True)
                            if  b < 30 and 10 * cp2 <= cash_balance:
                                cash_balance, stocks_owned = transact(
                                    cash_balance, stocks_owned, 10, cp2, True, False)
                            elif b > 70 and 10 <= stocks_owned:
                                cash_balance, stocks_owned = transact(
                                    cash_balance, stocks_owned, 10, cp2, False, True)
            if j == len(opvalues1) - 1 and k == len(opvalues2) - 1:
                cash_balance, stocks_owned = transact(
                    cash_balance, stocks_owned, stocks_owned, cp1, False, True)
                cash_balance, stocks_owned = transact(
                    cash_balance, stocks_owned, stocks_owned, cp2, False, True)
    

def transact(funds, stocks, qty, price, buy=False, sell=False):
    if buy == True and sell == False:
        if funds < qty * price:
            raise ValueError(f"Insufficient funds to purchase {qty} stock at ${price:0.2f}!")
        else:
            curfund = funds - qty * price
            curstock = stocks + qty
            return float(curfund), int(curstock)
    elif buy == False and sell == True:
        if stocks < qty:
            raise ValueError(f"Insufficient stock owned to sell {qty} stocks!")
        else:
            curfund = funds + qty * price
            curstock = stocks - qty
            return float(curfund), int(curstock)
    else:
        raise ValueError("Ambiguous transaction! Can't determine whether to buy or sell!")

    
