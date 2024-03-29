import pandas as pd
import yfinance as yf
from indicators import Indicators
from helperfunctions import trade


def main():
    cash = 1000000
    stocks = 0
    shorted_stocks = 0
    ticker = "BABA"
    start = "2008-01-01"
    end = "2022-12-31"

    data = prepare_data(ticker, start, end)

    for i in range(1,len(data)):
        row = data.iloc[i]
        prev_row = data.iloc[i-1]
        if prev_row.Position == 0 and row.Position == 1:
            stocks = cash / row.Price
            cash = 0
            shorted_stocks = 0
        elif prev_row.Position == 1 and row.Position == 0:
            cash = stocks * row.Price
            stocks = 0
            shorted_stocks = 0
        # elif prev_row.Position == 0 and row.Position == -1:
        #     # shorting
        #     shorted_stocks = cash / row.Price
        #     cash = 2 * cash
        #     stocks = 0
        # elif prev_row.Position == -1 and row.Position == 0:
        #     money = shorted_stocks * row.Price
        #     shorted_stocks = 0
        #     cash = cash - money
        #     stocks = 0
        elif prev_row.Position == -1 and row.Position == 1:
        #     money = shorted_stocks * row.Price
        #     cash = cash - money
        #     stocks = cash / row.Price 
        #     shorted_stocks = 0
        #     cash = 0
            stocks = cash / row.Price
            cash = 0
        elif prev_row.Position == 1 and row.Position == -1:
            # cash = stocks * 2 * row.Price
            # shorted_stocks = stocks
            # stocks = 0
            cash = stocks * row.Price
            stocks = 0
    print(f"Cash balance: {round(cash, 2)}")
    print(f"Stocks: {stocks}")
    print(f"Shorted stocs: {shorted_stocks}")

    

def prepare_data(ticker_symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    data = yf.download(ticker_symbol, start=start_date, end=end_date)
    data = data[["Adj Close"]]
    data = data.rename(columns={"Adj Close": "Price"})

    trade_signal_list = [0,]
    positions = [0,]
    pos = 0

    for i in range(1, len(data)):
        try:
            indicators = Indicators(data=data[:i], day="YESTERDAY")
            previous_indicators = Indicators(data=data[:i], day="DAY BEFORE YESTERDAY")
            rsi = indicators.rsi
            prev_rsi = previous_indicators.rsi
            sma = indicators.short_term_ma
            prev_sma = previous_indicators.short_term_ma
            lma = indicators.long_term_ma
            prev_lma = previous_indicators.long_term_ma
            trade_signal = trade(rsi,prev_rsi,sma,prev_sma,lma,prev_lma)

            if pos == 0 and trade_signal == 2:
                pos = 1
            elif pos == 0 and trade_signal == 1:
                pos = -1
            elif pos == 1 and trade_signal == 1:
                pos = -1
            elif pos == -1 and trade_signal == 2:
                pos = 1
            elif pos == 1 and trade_signal == -2:
                pos = 0
            elif pos == -1 and trade_signal == -1:
                pos = 0

            trade_signal_list.append(trade_signal)
            positions.append(pos)
        except:
            trade_signal_list.append(0)
            positions.append(0)

    data["Trade_suggestion"] = trade_signal_list
    data["Position"] = positions
    return data


if __name__ == "__main__":
    main()