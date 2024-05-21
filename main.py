import os
import logging
from dotenv import load_dotenv
from time import sleep

from data_treatment.treat_data import FileAnalyzer
from data_treatment.data_validate import JSONReader
from get_data import get_data_from_telegram as gd_telegram


ENV = load_dotenv()
if ENV:
    load_dotenv(ENV)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


class Main:
    def __init__(self):
        pass

    def run(self):
        while True:
            # First, get the data from Telegram
            gd_telegram.loop_main()
            # Then, validate the data
            file_analyzer = FileAnalyzer('group_messages.txt')
            json_reader = JSONReader('rescource/data.json')
            new_data = file_analyzer.find_pattern()
            if json_reader.read_json() == True and new_data != None:
                logging.info("Data read successfully.")
                json_reader.get_date_from_data(new_data)
                different_dates = json_reader.different_dates(date=json_reader.current_date)
                if different_dates:
                    # Finally, treat and save the new data
                    logging.info("Dates are different. Updating date and saving data.")
                    file_analyzer.save_to_json(data=new_data, file_path='rescource/data.json')
                else:
                    logging.info("Nothing to do. Waiting for the next iteration.")
            else:
                # Finally, treat and save the new data
                new_data = file_analyzer.find_pattern()
                if new_data != None:
                    logging.info("Data saved successfully.")
                    file_analyzer.save_to_json(data=new_data, filename='rescource/data.json')
            sleep(5)




if __name__ == "__main__":
    main = Main()
    main.run()