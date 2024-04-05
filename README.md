# Trade bot
The trading bot daily checks the stock data of the previous day and sends an email to either sell or buy a certain stock if the stock is a buy or sell. lambda_function.py file runs daily on AWS. To add or remove a subscriber subscription.py needs to be run.

How to use the program:
1. You need to create an AWS account
2. Run createtable.py to create a new table to store subscribers in AWS DynamoDB
3. Create a new lambda function and upload lambda_function.zip
4. Add 2 layers (python.zip and pandas.zip) to your lambda function
5. Add Financial Modeling Prep API, gmail, and AWS keys to the AWS Parameter store
6. Create a cron to run your lambda function daily
7. You can add or remove subscribers by running subscription.py on your local machine
8. backtest.py is for backtesting the trading strategy with historical stock data
