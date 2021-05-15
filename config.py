import logging

class Config:
    def __init__(self):
        self.Name = ""
        self.AmountHolding = ""

        # Live Coin Watch Scrape
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
