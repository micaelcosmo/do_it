import os
import logging
from dotenv import load_dotenv

# from data_treatment.treat_data import FileAnalyzer
# from data_treatment.data_validate import JSONReader
from get_data import get_data_from_telegram as gd_telegram


ENV = load_dotenv()
if ENV:
    load_dotenv(ENV)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


class Main:
    def __init__(self):
        pass

    def run(self):
        # First, get the data from Telegram
        gd_telegram.loop_main()



if __name__ == "__main__":
    main = Main()
    main.run()