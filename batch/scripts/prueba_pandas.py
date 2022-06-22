import pandas as pd

def run():
    archivo=pd.read_csv('unesco/whc-sites-2018-clean.csv')
    print(archivo)