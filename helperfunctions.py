import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import os
import boto3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib


def get_data(ticker: str) -> pd.DataFrame:
    """
    Downloads stock data and returns it as a pandas DataFrame.
    :param ticker: stock's ticker symbol.
    """
    end_date = datetime.now() - timedelta(days=1)
    end_date_str = end_date.strftime('%Y-%m-%d')

    start_date = end_date - timedelta(days=300)
    start_date_str = start_date.strftime('%Y-%m-%d')

    data = yf.download(ticker, start=start_date_str, end=end_date_str)
    data = data[["Adj Close"]]
    data = data.rename(columns={"Adj Close": "Price"})

    return data


def trade(rsi: float, previous_rsi: float, short_term_ma: float, previous_short_term_ma: float, long_term_ma: float, previous_long_term_ma: float) -> int:
    """
    Checks buy and sell conditions and returns 1 if stock is a buy, -1 if stock is a sell and 0 if stock is hold.
    :param rsi: yesterday's rsi value 
    :param previous_rsi: day's before yesterday rsi value 
    :param short_term_ma: yesterday's value of short term moving average 
    :param previous_short_term_ma: day's before yesterday value of short term moving average 
    :param long_term_ma: yesterday's value of long term moving average 
    :param previous_long_term_ma: day's before yesterday value of long term moving average 
    """
    # if (previous_rsi < 30 <= rsi) & (previous_short_term_ma < previous_long_term_ma) & (short_term_ma > long_term_ma):
    #     return 1
    
    # if (rsi <= 70 < previous_rsi) & (previous_short_term_ma > previous_long_term_ma) & (short_term_ma < long_term_ma):
    #     return -1
    
    # return 0
    if (previous_short_term_ma < previous_long_term_ma) & (short_term_ma > long_term_ma):
        return 2
    elif (previous_short_term_ma > previous_long_term_ma) & (short_term_ma < long_term_ma):
        return 1
    
    
    if (previous_rsi < 30 <= rsi):
        return -1
    elif (rsi <= 70 < previous_rsi):
        return -2
    
    return 0


def inform_subscribers(trade_result: int, ticker: str) -> None:
    """
    Sends email to the subscribers if today they need to either sell or buy the stock.
    :param trade: buy/sell indicator.
    :param ticker: a ticker symbol of the stock.
    """
    dynamodb = boto3.resource(
        "dynamodb",
        aws_access_key_id=os.environ.get("aws_access_key"),
        aws_secret_access_key=os.environ.get("aws_secret_access_key"),
        region_name="us-east-1"
    )
    
    table = dynamodb.Table("subscribers")
    response = table.scan()
    items = response["Items"]

    sender_email = "tcsprint2project@gmail.com"
    password = os.environ.get("TCgmail")
    if trade_result == 1:
        message_body = f"According to RSI and moving average indicators {ticker} stock is a buy"
    else:
        message_body = f"According to RSI and moving average indicators {ticker} stock is a sell"

    for item in items:

        receiver_email = item["Email"]
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = "Trade suggestion"

        message.attach(MIMEText(message_body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())