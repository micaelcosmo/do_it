import json
import logging
import time


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


class JSONReader:
    def __init__(self, file_path) -> None:
        self.file_path = file_path
        self.data : dict = {}
        self.last_date : str = ""
        self.current_date : str = ""

    def read_json(self) -> dict:
        """
        Reads the JSON file and returns the data as a dictionary.

        Returns:
            dict: The data read from the JSON file.
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.data = data
                return self.data
        except FileNotFoundError:
            logging.error(f"File '{self.file_path}' not found.")
            return None
        except json.JSONDecodeError:
            logging.error(f"Error decoding JSON file '{self.file_path}'.")
            return None

    def get_date_from_data(self) -> None:
        """
        Retrieves the last date from the data dictionary.
        """
        self.last_date = self.data.get('data_hora')
    
    def different_dates(self, date: str = '2024-05-21 01:04:26') -> bool:
        """
        Compares the last date with a given date and returns True if they are different.

        Args:
            date (str, optional): The date to compare with the last date. Defaults to '2024-05-21 01:04:26'.

        Returns:
            bool: True if the last date is different from the given date, False otherwise.
        """
        last_date = time.strptime(self.last_date, "%Y-%m-%d %H:%M:%S")
        current_date = time.strptime(date, "%Y-%m-%d %H:%M:%S")
        if last_date < current_date:
            logging.info("Last date is earlier than current date.")
            return True
        elif last_date > current_date:
            logging.info("Last date is later than current date.")
            return True
        else:
            logging.info("Dates are the same.")
            return False
    

if __name__ == '__main__':
    reader = JSONReader('data.json')
    data = reader.read_json()
    reader.get_date_from_data()
    different_dates = reader.different_dates('2024-05-21 02:04:21')
    logging.info(different_dates)
