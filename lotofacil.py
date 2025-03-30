from itertools import combinations
import os 
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pandas as pd

class Lotofacil:

    def __init__(self):
        self.path_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

        self.path_amostra = os.path.join(self.path_data, "amostra.pkl")
        
        self.path_lottery = os.path.join(self.path_data, "Lotofácil.xlsx")

    def generate_amostra(self):
        numeros = list(range(1, 26))
        combinacoes = list(combinations(numeros, 15))
        if not os.path.exists(self.path_amostra):
            with open(self.path_amostra, "wb") as file:
                pickle.dump(combinacoes, file)
            print("Arquivo amostra.pkl criado com sucesso.")
        else:
            print("Arquivo 'amostra.pkl' já existe.")
    
    def reading_amostra(self):
        with open(self.path_amostra, "rb") as file: 
            file = pickle.load(file)
            print("Leitura do arquivo 'amostra.pkl' feita com sucesso.")
            return file

    def search(self, file, numbers):
        if numbers in file:
            return True
        return False
    
    def position(self, file, numbers):
        for n, item in enumerate(file):
            if item == numbers:
                return [n, item]

    def save_lottery_numbers(self):
        options = webdriver.ChromeOptions()
        prefs = {"download.default_directory": self.path_data,}
        options.add_experimental_option("prefs", prefs)
        if not os.path.exists(self.path_lottery):
            with webdriver.Chrome(options=options) as driver:
                driver.get("https://loterias.caixa.gov.br/Paginas/Lotofacil.aspx")

                button = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="btnResultados"]'))
                )
                button.click()
                sleep(2)
            print("Arquivo 'Lotofácil.xlsx' criado com sucesso.")
        else:
            print("Arquivo 'Lotofácil.xlsx' já existe.")

    def get_lottery_results(self):
        """
        'Concurso', 'Data Sorteio', 'Bola1', 'Bola2', 'Bola3', 'Bola4', 'Bola5',
        'Bola6', 'Bola7', 'Bola8', 'Bola9', 'Bola10', 'Bola11', 'Bola12',       
        'Bola13', 'Bola14', 'Bola15', 'Ganhadores 15 acertos', 'Cidade / UF',   
        'Rateio 15 acertos', 'Ganhadores 14 acertos', 'Rateio 14 acertos',      
        'Ganhadores 13 acertos', 'Rateio 13 acertos', 'Ganhadores 12 acertos',  
        'Rateio 12 acertos', 'Ganhadores 11 acertos', 'Rateio 11 acertos',      
        'Acumulado 15 acertos', 'Arrecadacao Total', 'Estimativa Prêmio',       
        'Acumulado sorteio especial Lotofácil da Independência', 'Observação'
        """
        return pd.read_excel(self.path_lottery)


    
if __name__ == "__main__":
    lotofacil = Lotofacil()
    lotofacil.generate()

    # file = lotofacil.reading()

    # numbers = (1, 2, 4, 6, 7, 8, 9, 13, 17, 19, 20, 21, 22, 24, 25)
    # print(lotofacil.position(file, numbers))

    # amostra_total.save_lottery_numbers()
    print(lotofacil.get_lottery_results().columns)
