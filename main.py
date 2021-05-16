from bs4 import BeautifulSoup
from datetime import datetime
import requests
import logging
import json
import time
import sys
import os
import re
from config import Config


class Connector:
    def __init__(self):
        # Moved prototypes to its own file because it started getting long
        self.config = Config()

    def getPyePrice(self):
        logging.info("Connecting to livewatchcoin.com to get CreamPye Price")
        URL = f'https://api.pancakeswap.info/api/tokens/{self.config.PyeAddr}'
        page = requests.get(URL)

        if page.status_code != 200:
            logging.error(page.status_code)
        else:
            logging.info(page.status_code)

        self.config.PyePrice = json.loads(page.text)["data"]["price"]
        return self.config.PyePrice

    def getPyeHodlers(self):
        logging.info("Connecting to bscscan to get CreamPye hodlers")

        URL = 'https://bscscan.com/token/0xaad87f47cdea777faf87e7602e91e3a6afbe4d57'
        page = requests.get(URL)

        if page.status_code != 200:
            logging.error(page.status_code)
        else:
            logging.info(page.status_code)

        soup = BeautifulSoup(page.content, 'html.parser')
        self.config.PyeHodlers = soup.find('div', class_='mr-3').get_text().split("<")[0].strip("$")
        return self.config.PyeHodlers


def main():
    connector = Connector()

    print(os.path.exists("./user_profile.pye"))

    try:
        if os.path.exists("./user_profile.pye"):
            with open("user_profile.pye", "r") as fp:
                entries = fp.readlines()
                connector.config.Name = entries[0]
                connector.config.AmountHolding = entries[1]

        else:
            print("No user profile found, creating...")
            with open("user_profile.pye", "w+") as fp:
                connector.config.Name = input("Enter a name: ")
                while True:
                    print("Enter the amount of Pye you have (as a whole number)")
                    connector.config.AmountHolding = input("In the future, you'll simply have to connect \nyour wallet address and this will be automated: ")
                    if not re.findall("[+-]?[0-9]+", connector.config.AmountHolding):
                        print("Please enter the amount of Pye you have as a whole number (No decimals): ")
                    else:
                        break

                fp.write(f"{connector.config.Name}\n")
                fp.write(connector.config.AmountHolding)

    except IndexError:
        print("User Profile Error, cleaning up, please relaunch!!")
        os.remove("user_profile.pye")
        # TODO: Make program relaunch itself here
        # os.execv(sys.executable, ['python'] + sys.argv)

    while True:
        price = float(connector.getPyePrice()) * int(connector.config.AmountHolding)

        priceChange = connector.config.PyePriceChangeHour
        hodlers = connector.getPyeHodlers()
        banner = """
--------------------------------
Welcome, {name}

Current Time: {time}   
Current Wallet Value: ${price}
Current Pye Hodlers: {hodlers}

--------------------------------""".format(name=connector.config.Name,
                                           price=price,
                                           time=datetime.now(),
                                           priceChange=priceChange,
                                           hodlers=hodlers.strip("\n"))
        print(banner)
        time.sleep(20)


if __name__ == "__main__":
    main()


# TODO:
#   -Full logging
#   -Encrypt user_profile.pye
#   -Password for returning users
#   -Move onto other coins eventually?
#   -Full GUI LOL
