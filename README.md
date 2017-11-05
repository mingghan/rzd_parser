## Description
Parse rzd.ru to catch train tickets

This tool parses pass.rzd.ru site every 10 minutes and notifies user in Telegram, if a ticket occurs

## Usage
### Preparation
In order to use this tool you need to take some preparation steps:
0. Install Mozilla Firefox browser
1. Install selenium webdriver
`pip install selenium`
2. Install request library
`pip install requests`
3. Create Telegram bot and get token

### Tool
1. `git clone https://github.com/mingghan/rzd_parser.git`
2. Put your Telegram bot token into `config.py`
3. Run `python parse_rzd <url> <ticket type to find>`
For example, `python parse_rzd.py "https://pass.rzd.ru/tickets/public/ru?STRUCTURE_ID=704&refererPageId=4819&layer_name=e3-route&tfl=3&st0=МОСКВА&code0=2000000&dt0=05.11.2017&st1=ЯРОСЛАВЛЬ&code1=2010000&checkSeats=1" "Сидячий"`
4. Script is going to parse the page to find specified ticket every 10 minutes and notify you in Telegram
