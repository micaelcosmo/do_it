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


class AnalisadorArquivo:
    def __init__(self, nome_arquivo):
        self.nome_arquivo = nome_arquivo
        

    def encontrar_padrao(self):
        """
        Find and extract patterns from the file.

        Returns:
            dict: A dictionary containing the extracted data.
        """
        with open(self.nome_arquivo, 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()
            padrao_inicio = fr"{target_phone_number}{pattern_start}"
            indice_inicio = linhas.index(padrao_inicio + "\n") + 1
            quantidade_linhas = 13  # Defina a quantidade de linhas que você deseja após o início do padrão
            dados_tratados = {}
            if indice_inicio != -1:
                logging.info("PADRÃO ENCONTRADO - INÍCIO")
                for linha in linhas[indice_inicio:indice_inicio+quantidade_linhas]:
                    if re.match(fr"{pattern_roleta}", linha):
                        dados_tratados['roleta'] = re.search(fr"{pattern_roleta}", linha).group(1)
                        logging.debug("Roleta: %s", re.search(fr"{pattern_roleta}", linha).group(1))
                    elif re.match(fr"{pattern_estrategia}", linha):
                        dados_tratados['estrategia'] = re.search(fr"{pattern_estrategia}", linha).group(1)
                        logging.debug("Estratégia: %s", re.search(fr"{pattern_estrategia}", linha).group(1))
                    elif re.match(fr"{pattern_apostar}", linha):
                        dados_tratados['apostar'] = re.search(fr"{pattern_apostar}", linha).group(1)
                        logging.debug("Apostar: %s", re.search(fr"{pattern_apostar}", linha).group(1))
                    elif re.match(fr"{pattern_numeros}", linha):
                        numeros = re.search(fr"{pattern_numeros}", linha).group(1).strip().replace("**", "").split(" | ")
                        dados_tratados['numeros'] = [int(numero) for numero in numeros]
                        logging.debug("Números: %s", numeros)
                    elif re.match(fr"{pattern_cobrir_zero}", linha):
                        dados_tratados['cobrir_zero'] = re.search(fr"{pattern_cobrir_zero}", linha).group(1).replace("**", "")
                        logging.debug("Cobrir Zero: %s", re.search(fr"{pattern_cobrir_zero}", linha).group(1).replace("**", ""))
                    elif re.match(fr"{pattern_link}", linha):
                        dados_tratados['link'] = re.search(fr"{pattern_link}", linha).group(1)
                        logging.debug("Link: %s", re.search(fr"{pattern_link}", linha).group(1))
                    elif re.match(fr"{pattern_data_hora}", linha):
                        dados_tratados['data_hora'] = re.match(fr"{pattern_data_hora}", linha).group().format("YYYY-MM-DD HH:mm:ss")
                        logging.debug("Data e Hora: %s", re.match(fr"{pattern_data_hora}", linha).group())
                logging.info(json.dumps(dados_tratados, indent=4, ensure_ascii=False))
                logging.info("PADRÃO ENCONTRADO - FIM")
                return dados_tratados
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
    analise = AnalisadorArquivo("group_messages.txt")
    data = analise.encontrar_padrao()
    analise.save_to_json(data, "data.json")
