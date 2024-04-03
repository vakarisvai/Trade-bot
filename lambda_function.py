from helperfunctions import get_data, trade, inform_subscribers
from indicators import Indicators

def lambda_handler():
    ticker = "MCO"

    data = get_data(ticker=ticker)

    indicators = Indicators(data=data, day="YESTERDAY")
    previous_indicators = Indicators(data=data, day="DAY BEFORE YESTERDAY")

    trade_suggestion: int = trade(
        rsi=indicators.rsi,
        previous_rsi=previous_indicators.rsi,
        short_term_ma=indicators.short_term_ma,
        previous_short_term_ma=previous_indicators.short_term_ma,
        long_term_ma=indicators.long_term_ma,
        previous_long_term_ma=previous_indicators.long_term_ma,
    )

    if trade_suggestion in [-1, 1]:
        inform_subscribers(trade_result=trade_suggestion, ticker=ticker)