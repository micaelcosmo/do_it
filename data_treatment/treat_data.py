import re
import os
import json
import logging
from dotenv import find_dotenv, load_dotenv


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
# Load environment variables from .env file
ENV = find_dotenv()
if ENV:
    load_dotenv(ENV)
# Settings and constants
target_phone_number = os.getenv('TARGET_PHONE_NUMBER')
pattern_start = os.getenv('PATTERN_START')
pattern_roleta = os.getenv('PATTERN_ROLETA')
pattern_estrategia = os.getenv('PATTERN_ESTRATEGIA')
pattern_apostar = os.getenv('PATTERN_APOSTAR')
pattern_numeros = os.getenv('PATTERN_NUMEROS')
pattern_cobrir_zero = os.getenv('PATTERN_COBRIR_ZERO')
pattern_link = os.getenv('PATTERN_LINK')
pattern_data_hora = os.getenv('PATTERN_DATA_HORA')


class FileAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        

    def find_pattern(self):
        """
        Find and extract patterns from the file.

        Returns:
            dict: A dictionary containing the extracted data.
        """
        with open(self.file_path, 'r', encoding='utf-8') as arquivo:
            lines = arquivo.readlines()
            pattern_start_string = fr"{target_phone_number}{pattern_start}"
            start_index = lines.index(pattern_start_string + "\n") + 1
            line_count = 13  # Defina a quantidade de lines que você deseja após o início do padrão
            treated_data = {}
            if start_index != -1:
                logging.info("PADRÃO ENCONTRADO - INÍCIO")
                for linha in lines[start_index:start_index+line_count]:
                    if re.match(fr"{pattern_roleta}", linha):
                        treated_data['roleta'] = re.search(fr"{pattern_roleta}", linha).group(1)
                        logging.debug("Roleta: %s", re.search(fr"{pattern_roleta}", linha).group(1))
                    elif re.match(fr"{pattern_estrategia}", linha):
                        treated_data['estrategia'] = re.search(fr"{pattern_estrategia}", linha).group(1)
                        logging.debug("Estratégia: %s", re.search(fr"{pattern_estrategia}", linha).group(1))
                    elif re.match(fr"{pattern_apostar}", linha):
                        treated_data['apostar'] = re.search(fr"{pattern_apostar}", linha).group(1)
                        logging.debug("Apostar: %s", re.search(fr"{pattern_apostar}", linha).group(1))
                    elif re.match(fr"{pattern_numeros}", linha):
                        numeros = re.search(fr"{pattern_numeros}", linha).group(1).strip().replace("**", "").split(" | ")
                        treated_data['numeros'] = [int(numero) for numero in numeros]
                        logging.debug("Números: %s", numeros)
                    elif re.match(fr"{pattern_cobrir_zero}", linha):
                        treated_data['cobrir_zero'] = re.search(fr"{pattern_cobrir_zero}", linha).group(1).replace("**", "")
                        logging.debug("Cobrir Zero: %s", re.search(fr"{pattern_cobrir_zero}", linha).group(1).replace("**", ""))
                    elif re.match(fr"{pattern_link}", linha):
                        treated_data['link'] = re.search(fr"{pattern_link}", linha).group(1)
                        logging.debug("Link: %s", re.search(fr"{pattern_link}", linha).group(1))
                    elif re.match(fr"{pattern_data_hora}", linha):
                        treated_data['data_hora'] = re.match(fr"{pattern_data_hora}", linha).group().format("YYYY-MM-DD HH:mm:ss")
                        logging.debug("Data e Hora: %s", re.match(fr"{pattern_data_hora}", linha).group())
                logging.info(json.dumps(treated_data, indent=4, ensure_ascii=False))
                logging.info("PADRÃO ENCONTRADO - FIM")
                return treated_data
            else:
                logging.info("Padrão não encontrado.")
                return None
    
    @staticmethod
    def save_to_json(data, file_path):
        """
        Save data to a JSON file.

        Args:
            data (dict): The data to be saved.
            file_path (str): The path to the JSON file.

        Returns:
            None
        """
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    analise = FileAnalyzer("group_messages.txt")
    data = analise.find_pattern()
    analise.save_to_json(data, "data.json")
