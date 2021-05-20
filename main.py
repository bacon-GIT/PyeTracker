import tkinter as tk
from PIL import Image, ImageTk
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import logging
import json
import time
import os
import re
from config import Config


class App():
    def __init__(self):
        # Moved prototypes to its own file because it started getting long
        self.config = Config()


    def startApp(self):
        self.root = tk.Tk()
        self.root.title("CreamPYE Tracker")
        self.root.geometry("300x300")

        logging.info(os.path.exists("./user_profile.pye"))

        try:
            if os.path.exists("./user_profile.pye"):
                with open("user_profile.pye", "r") as fp:
                    entries = fp.readlines()
                    self.config.Name = entries[0]
                    self.config.AmountHolding = entries[1]

            else:
                print("No user profile, creating...")
                self.userprofilelabel = tk.Label(text="", fg="white", bg="black")
                self.userprofilelabel.pack()
                with open("user_profile.pye", "w+") as fp:
                    self.config.Name = input("Please enter a name: ")
                    while True:
                        print("Enter the amount of Pye you have (as a whole number)")
                        self.config.AmountHolding = input(
                            "In the future, you'll simply have to connect \nyour wallet address and this will be automated: ")
                        if not re.findall("[+-]?[0-9]+", self.config.AmountHolding):
                            print("Please enter the amount of Pye you have as a whole number (No decimals): ")
                        else:
                            break

                    fp.write(f"{self.config.Name}\n")
                    fp.write(self.config.AmountHolding)

        except IndexError:
            print("User Profile Error, cleaning up, please relaunch!!")
            os.remove("user_profile.pye")
            # TODO: Make program relaunch itself here
            # os.execv(sys.executable, ['python'] + sys.argv)

        self.root['bg'] = "black"
        self.label = tk.Label(text="", fg="white", bg="black")
        self.canvas = tk.Canvas(self.root, width=150, height=150, bg="black", highlightthickness=0)
        self.canvas.pack()
        self.canvas.place(x=10, y=200)
        image = Image.open("assets/logo.png")
        resize_image = image.resize((70, 70))
        self.img = ImageTk.PhotoImage(resize_image)
        self.canvas.create_image(40, 40, anchor=tk.CENTER, image=self.img)

        self.label.place(relx=0.0,
                         rely=0.0,
                         anchor='sw')
        self.label.pack()

        #self.logolabel.place(relx=1.0,
        #                     rely=1.0,
        #                     anchor='sw')
        #self.logolabel.pack()
        self.update_clock()
        self.root.mainloop()

    def update_clock(self):

        price = float(self.getPyePrice()) * int(self.config.AmountHolding)
        priceChange = self.config.PyePriceChangeHour
        hodlers = self.getPyeHodlers()
        banner = r"""
Welcome {name}
{time}      
~~~~~~~~
Wallet Value: ${price}
Pye Hodlers: {hodlers}
""".format(name=self.config.Name,
           price=str(price)[:9],
           time=datetime.now(),
           priceChange=priceChange,
           hodlers=hodlers.strip("\n"))
        self.label.configure(text=banner)
        self.root.after(1000, self.update_clock)

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
    connector = App()
    connector.startApp()


if __name__ == "__main__":
    main()


# TODO:
#   -Full logging
#   -Encrypt user_profile.pye
#   -Password for returning users
#   -Move onto other coins eventually?
#   -Full GUI LOL
