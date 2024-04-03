import requests
import pandas as pd
import boto3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from indicators import Indicators


def get_data(ticker: str) -> pd.DataFrame:
    """
    Downloads stock data and returns it as a pandas DataFrame.
    :param ticker: stock's ticker symbol.
    """
    ssm_client = boto3.client("ssm")
    api_key = ssm_client.get_parameter(Name="fmp_key", WithDecryption=True)["Parameter"]["Value"]

    url = f'https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?apikey={api_key}'
    response = requests.get(url)

    data = response.json()['historical']
    data = pd.DataFrame(data)
    data['date'] = pd.to_datetime(data['date'])
    data.set_index('date', inplace=True)
    data = data[['close']]
    data.columns = ['Price']
    period = Indicators.long_term_window + 5
    data = data[-period:]

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
    ssm_client = boto3.client('ssm')
    aws_access_key = ssm_client.get_parameter(Name="my_aws_access_key", WithDecryption=True)["Parameter"]["Value"]
    aws_secret_access_key = ssm_client.get_parameter(Name="my_aws_secret_access_key", WithDecryption=True)["Parameter"]["Value"]
    gmail_password = ssm_client.get_parameter(Name="tc_gmail_key", WithDecryption=True)["Parameter"]["Value"]

    dynamodb = boto3.resource(
        "dynamodb",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_access_key,
        region_name="us-east-1"
    )
    
    table = dynamodb.Table("subscribers")
    response = table.scan()
    items = response["Items"]

    sender_email = "tcsprint2project@gmail.com"
    password = gmail_password
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