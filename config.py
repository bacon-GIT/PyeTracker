import logging

class Config:
    def __init__(self):
        self.Name = ""
        self.AmountHolding = ""

        # API Scrape
        self.PyeAddr = "0xaad87f47cdea777faf87e7602e91e3a6afbe4d57"
        self.PyePrice = 0
        self.PyePriceChangeHour = ""
        self.PyePriceChangeDay = ""
        self.PyePriceChangeWeek = ""
        self.PyeMarketCap = ""
        self.PyeVolume = ""

        # BSCSCAN Scrape
        self.PyeHodlers = 0

        # Twitter Scrape
        self.LatestTweet = ""

        logging.basicConfig(level=logging.INFO,
                            filename="threatfeed.log",
                            filemode="a",
                            format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        

