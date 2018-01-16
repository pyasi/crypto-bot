# crypto-bot
Crypto currency slackbot for getting info and storing your own portfolio

Currently a WiP, more functionality to come.

## Functions

This slackbot gives you the ability to view current data on all coins, as well as maintain your own personal crypto portfolio.

 - Query the status of a coin to get all current information using slash commands
 - Add to and view your own portfolio
 - List all coins and their tickers
 - Ability to interact with the bot via slash commans, @mentions, or direct messages with the bot
 
 
## Examples
 
#### Single coin
 ```
/coin [ticker]
 ```

###### Positive
![Alt text](screenshots/Single-coin-positive.png "Single Coin Positive")

###### Negative
![Alt text](screenshots/Single-coin-negative.png "Single Coin Negative")

#### Portfolio
 ```
/Portfolio [ticker] [amount]
 ``` 
 
 To add/alter portfolio and then view it
 
 Or
 
 ```
@cryptobot portfolio
 ``` 
 
 To just view it
 
![Alt text](screenshots/Portfolio.png "Portfolio")

#### All coins
 ```
@cryptobot coins
 ``` 
 
 or DM bot directly
 
![Alt text](screenshots/List-all-coins.png "All Coins")

#### Help
 ```
@cryptobot help
 ``` 
 
 or DM bot directly
 
![Alt text](screenshots/Help-menu.png "Help Menu")

### Prerequisites

All requirements are in the requirements.txt file

```
pip install -r requirements.txt
```


