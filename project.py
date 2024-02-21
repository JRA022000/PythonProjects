from tabulate import tabulate
from datetime import date
import yfinance as yf
import requests
import sys
import os
import csv

def print_table(portfolio: dict):
    """
    Prints the current portfolio as a table.

    :param portfolio: The current portfolio
    :type portfolio: dict
    :return: Does not return
    """
    os.system('clear')
    print(tabulate(portfolio,tablefmt="grid"))
    ret=input("Press enter to return to main menu")
    return

def stock_lookup(look_up: str):
     """
    Looks up a stock price using an API

    :param look_up: Symbol of the stock to look up
    :type look_up: Str
    :raise KeyError: If stock does not have a current price, returns 0.0
    :raise RequestException: if stock symbol does not exit, returns -1.0
    :return: A float indicating stock price, 0.0 is no stock price available, -1.0 if invalid stock price provided.
    """
     try:
        ticker=yf.Ticker(look_up)
        try:
           return(ticker.info["currentPrice"])
        except (KeyError):
            return(0.0)
     except (requests.RequestException):
            return(-1.00)


def purchase(portfolio: dict, purchased_symbol: str, purchased_quantity:str, purchased_price: float):
    """
    Adds a purchased stock to the portfolio
    :param portfolio: The current portfolio
    :type portfolio: dict
    :param purchased_symbol: The stock symbol of the stock to be purchased
    :type portfolio: str
    :param purchased_quantity: The amount of shares purchased
    :type portfolio: str
    :param purchased_price: The purchased price of the stock, found using the api
    :type portfolio: str
    :return: Returns a confirmation string
    """
    purchased_date=date.today()
    portfolio.append({"purchase_date": purchased_date, "symbol": purchased_symbol, "quantity": purchased_quantity, "purchase_price": purchased_price})
    return("Purchase confirmed and updated to portfolio")


def sell(portfolio: dict, sold: str):
    """
    Adds a purchased stock to the portfolio
    :param portfolio: The current portfolio
    :type portfolio: dict
    :param sold: The stock symbol of the stock to be purchased
    :type sold: str
    :return: Returns a boolean which represents the presence of the stock in the current portfolio
    """
    sold_found=False
    for s in range(len(portfolio)-1):
        if portfolio[s]["symbol"]== sold:
            del portfolio[s]
            sold_found=True
    return sold_found

def main():
    portfolio=[]
    try:
        with open("portfolio.csv",newline='') as file_in:
            reader= csv.DictReader(file_in)
            for row in reader:
                portfolio.append({"purchase_date": row["purchase_date"], "symbol": row["symbol"], "quantity": row["quantity"], "purchase_price":row["purchase_price"]})
    except (FileNotFoundError):
        print("Porfolio file not found, creating now.")
        file = open("portfolio.csv","a")
        file.close()
        ret=input("Press enter to return to main menu")
    main_menu=[
        {"Option": "A", "Action":"Get stock price"},
        {"Option": "B", "Action":"Show current prortfolio"},
        {"Option": "C", "Action":"Purchase and add to portfolio"},
        {"Option": "D", "Action":"Sell and remove from portfolio"},
        {"Option": "E", "Action":"Exit program"}
                ]
    while True:
        os.system('clear')
        print(tabulate(main_menu,tablefmt="grid"))
        choice=input("Enter: ").strip().upper()
        match choice:
            case "A":
                look_up=input("Enter the symbol of the stock you want to look up: ")
                value=stock_lookup(look_up)
                if value==-1.0:
                    print("Invalid stock symbol")
                elif value==0.00:
                    print("Stock price not currently available")
                else:
                    print(f"The current price of the stock is ${value:.2f}")
                    for s in range(len(portfolio)):
                        if portfolio[s]["symbol"]== look_up:
                            print("This stock is in your portfolio")
                            original_price=portfolio[s]["purchase_price"]
                            original_price=float(original_price)
                            current_price=float(value)
                            profit=float(current_price-original_price)
                            if profit>0:
                                print(f"If you sold this stock, your profit would be ${profit:.2f} per share" )
                            elif profit==0:
                                print(f"You own this stock at the current price of ${current_price:.2f} per share")
                            else:
                                print(f"If you sold this stock, your loss would be ${profit:.2f} per share" )
                ret=input("Press enter to return to main menu")
            case "B":
                print_table(portfolio)
            case "C":
                while True:
                    purchased_symbol=input("Symbol of stock purchased: ")
                    purchased_symbol=purchased_symbol.upper()
                    try:
                        ticker=yf.Ticker(purchased_symbol)
                        purchased_price=float(ticker.info["currentPrice"])
                        print(f"Current price is ${purchased_price:.2f} per share")
                        break
                    except (requests.RequestException):
                        print("Invalid stock symbol entered")
                        pass
                purchased_quantity=input("Number of shares purchased: ")
                if purchased_symbol =='' or purchased_quantity=='':
                    print("Invalid Entry detected")
                print(purchase(portfolio, purchased_symbol, purchased_quantity, purchased_price))
                with open("portfolio.csv","w") as file_out:
                    writer=csv.DictWriter(file_out, fieldnames=["purchase_date","symbol","quantity","purchase_price"])
                    writer.writeheader()
                    for s in portfolio:
                        writer.writerow({"purchase_date":s["purchase_date"],"symbol":s["symbol"], "quantity":s["quantity"], "purchase_price":s["purchase_price"]})
                ret=input("Press enter to return to main menu")
            case "D":
                sold=input("Enter symbol of stock sold :")
                sold=sold.upper()
                if sell(portfolio,sold):
                        print("Stock removed from portfolio")
                        with open("portfolio.csv","w") as file_out:
                            writer=csv.DictWriter(file_out, fieldnames=["purchase_date","symbol","quantity","purchase_price"])
                            writer.writeheader()
                            for s in portfolio:
                                writer.writerow({"purchase_date":s["purchase_date"],"symbol":s["symbol"], "quantity":s["quantity"], "purchase_price":s["purchase_price"]})
                else:
                    print("Stock not in portfolio")
                ret=input("Please enter to return to main menu")
            case "E":
                sys.exit()
            case _:
                print("Invalid Entry")
                ret=input("Press enter to return to main menu")
                pass



if __name__=="__main__":
    main()